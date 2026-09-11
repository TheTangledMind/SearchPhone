import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import search_phone
from i18n import Translator


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        env = patch.dict(os.environ, {'XDG_CONFIG_HOME': self.temp.name})
        env.start()
        self.addCleanup(env.stop)
        network = patch('requests.get', side_effect=AssertionError('No network in tests'))
        network.start()
        self.addCleanup(network.stop)

    def menu(self, answers):
        output = io.StringIO()
        with patch('builtins.input', side_effect=answers), contextlib.redirect_stdout(output):
            search_phone.main()
        return output.getvalue()

    def test_menu_changes_language_and_restores_on_restart(self):
        output = self.menu(['2', '2', '0'])
        self.assertIn('1. Search phone number', output)
        self.assertIn('Idioma guardado', output)
        self.assertIn('1. Buscar número de teléfono', output)
        self.assertIn('1. Buscar número de teléfono', self.menu(['0']))

    def test_menu_scan_uses_selected_language(self):
        Translator().set_language('es', persist=True)
        with contextlib.chdir(self.temp.name), patch.object(search_phone.PhoneOSINT, 'analyze_phone', autospec=True) as scan:
            self.menu(['1', '+12025550123', 'us', '0'])
        instance, number, region = scan.call_args.args
        self.assertEqual(instance.tr.language, 'es')
        self.assertEqual((number, region), ('+12025550123', 'us'))

    def test_bad_menu_choice_and_eof_do_not_scan(self):
        with patch.object(search_phone.PhoneOSINT, 'analyze_phone') as scan:
            self.assertIn('Invalid choice', self.menu(['nonsense', '0']))
            with patch('builtins.input', side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()):
                search_phone.main()
            scan.assert_not_called()

    def test_reports_follow_language_and_keep_json_keys(self):
        for code, title, pdf_title in [('en', 'FULL REPORT', 'SearchPhone OSINT - Report'), ('es', 'REPORTE COMPLETO', 'SearchPhone OSINT - Reporte')]:
            with self.subTest(language=code), contextlib.chdir(self.temp.name):
                app = search_phone.PhoneOSINT(language=code)
                app.report_dir = str(Path(self.temp.name) / code)
                Path(app.report_dir).mkdir()
                app.phone_number, app.region, app.timestamp = '+12025550123', 'us', 'test'
                app.results['phone_info'] = app.validate_phone(app.phone_number, 'us')
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    app.display_results()
                    app.export_results()
                    app.export_pdf()
                self.assertIn(title, output.getvalue())
                data = json.loads((Path(app.report_dir) / app.get_filename('json')).read_text())
                self.assertEqual(data['metadata']['language'], code)
                self.assertIn('phone_info', data['results'])
                if search_phone.PDF_AVAILABLE and shutil.which('pdftotext'):
                    pdf = Path(app.report_dir) / app.get_filename('pdf')
                    text = subprocess.check_output(['pdftotext', str(pdf), '-']).decode()
                    self.assertIn(pdf_title, text)
                    self.assertIn('Teléfono:' if code == 'es' else 'Phone:', text)
