"""Language catalogues and a per-user preference; no credentials are stored here."""
import json
import os
from pathlib import Path
import tempfile

DEFAULT_LANGUAGE = 'en'
LOCALES = Path(__file__).resolve().parent / 'locales'


def available_languages():
    languages = []
    for path in sorted(LOCALES.glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        languages.append((path.stem, data['language_name']))
    return languages


def settings_path():
    root = os.environ.get('XDG_CONFIG_HOME')
    base = Path(root) if root and Path(root).is_absolute() else Path.home() / '.config'
    return base / 'searchphone' / 'settings.json'


def saved_language():
    try:
        data = json.loads(settings_path().read_text(encoding='utf-8'))
        language = data.get('language') if isinstance(data, dict) else None
        if isinstance(language, str) and language in dict(available_languages()):
            return language
    except (OSError, ValueError):
        pass
    return DEFAULT_LANGUAGE


def save_language(language):
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(prefix='.settings-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump({'language': language}, handle)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Translator:
    def __init__(self, language=None):
        self.fallback = self._catalog(DEFAULT_LANGUAGE)
        self.set_language(language if language is not None else saved_language())

    @staticmethod
    def _catalog(language):
        return json.loads((LOCALES / f'{language}.json').read_text(encoding='utf-8'))['messages']

    def set_language(self, language, *, persist=False):
        if language not in dict(available_languages()):
            raise ValueError('Unsupported language')
        messages = self._catalog(language)
        if persist:
            save_language(language)
        self.language = language
        self.messages = messages

    def __call__(self, key, **values):
        template = self.messages.get(key, self.fallback.get(key, key))
        return template.format(**values)
