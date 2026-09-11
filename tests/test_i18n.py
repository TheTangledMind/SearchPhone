import json
import os
from string import Formatter
import tempfile
import unittest
from unittest.mock import patch

from i18n import Translator, available_languages, settings_path


class LanguageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        env = patch.dict(os.environ, {'XDG_CONFIG_HOME': self.temp.name})
        env.start()
        self.addCleanup(env.stop)

    def test_default_and_saved_language(self):
        tr = Translator()
        self.assertEqual(tr.language, 'en')
        self.assertEqual(tr('menu.search'), '1. Search phone number')
        tr.set_language('es', persist=True)
        self.assertEqual(tr('menu.search'), '1. Buscar número de teléfono')
        self.assertEqual(Translator().language, 'es')
        self.assertEqual(json.loads(settings_path().read_text()), {'language': 'es'})
        self.assertEqual(settings_path().stat().st_mode & 0o777, 0o600)

    def test_invalid_setting_uses_english(self):
        settings_path().parent.mkdir(parents=True)
        for raw in ['broken json', '[]', '{"language":"unknown"}', '{"language":[]}']:
            settings_path().write_text(raw)
            self.assertEqual(Translator().language, 'en')

    def test_invalid_language_is_rejected(self):
        tr = Translator('es')
        with self.assertRaises(ValueError):
            tr.set_language('../other', persist=True)
        self.assertEqual(tr.language, 'es')
        self.assertFalse(settings_path().exists())

    def test_save_failure_preserves_language(self):
        tr = Translator('en')
        with patch('i18n.os.replace', side_effect=OSError('read-only')):
            with self.assertRaises(OSError):
                tr.set_language('es', persist=True)
        self.assertEqual(tr.language, 'en')
        self.assertFalse(settings_path().exists())
        self.assertEqual(list(settings_path().parent.iterdir()), [])

    def test_catalogue_keys_and_placeholders(self):
        codes = [code for code, _ in available_languages()]
        self.assertIn('en', codes)
        self.assertIn('es', codes)
        catalogs = [Translator(code).messages for code in codes]
        for catalog in catalogs[1:]:
            self.assertEqual(catalogs[0].keys(), catalog.keys())
        def fields(value):
            return {field for _, field, _, _ in Formatter().parse(value) if field is not None}
        for catalog in catalogs[1:]:
            for key in catalogs[0]:
                self.assertEqual(fields(catalogs[0][key]), fields(catalog[key]), key)

    def test_missing_translation_falls_back(self):
        tr = Translator('es')
        tr.messages = dict(tr.messages)
        tr.messages.pop('menu.search')
        self.assertEqual(tr('menu.search'), '1. Search phone number')
