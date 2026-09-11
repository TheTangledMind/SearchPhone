# SearchPhone — fork

We forked [SearchPhone by Victor Bancayan / Hack Underway](https://github.com/HackUnderway/SearchPhone)
with the intention of building on its phone-number OSINT features and exploring
how its search and reporting capabilities can complement our PhoneInfoga work.

Credit for the original project belongs to Victor Bancayan / Hack Underway.
Original MIT licensing is preserved: [LICENSE](LICENSE).

SearchPhone combines phone-number metadata with searches through Numverify,
SerpAPI, GitHub, Reddit, DuckDuckGo and a Hudson Rock lookup. It can export JSON
and PDF reports. Results are investigative leads, not verified ownership. The
Hudson Rock code uses a username-search endpoint with the supplied number; this
is not proof that a phone or its owner was compromised.

## Local setup and usage

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp example.env .env
```

Edit the ignored `.env` locally with the provider values you need:
`NUMVERIFY_KEY`, `SERPAPI_KEY`, and `GITHUB_TOKEN`. Never commit real credentials.
Alternatively keep them outside the repo and load that file explicitly:

```bash
python -m dotenv -f /path/to/private.env run -- python search_phone.py
```

With a local `.env`:

```bash
python search_phone.py
```

Choose **1. Search phone number** from the menu, then enter the phone number and
country/region. Use only numbers you are authorized to investigate. Searches disclose query data to external services.
Reports are written under the ignored `reports/` directory and may contain
personal information; review them before sharing.

Run `search_phone.py` directly. The copied `src/` package entry point is currently
a placeholder and does not run this tool. The existing packaging files have not
been rewritten as part of the README cleanup.

## Language settings

The interface starts in **English** unless you have saved another language.
Choose **2. Language / Idioma**, then choose **English** or **Español**. The change
applies immediately and becomes the default on the next launch. Choose **0** to
cancel language selection or exit the main menu. After a search, the main menu
returns so you can change language or run another search.

The selected language is stored in `~/.config/searchphone/settings.json`, or
`$XDG_CONFIG_HOME/searchphone/settings.json` when that variable names an absolute
path. This separate user preference contains no API keys, is outside the repo by
default, and is created with owner-only permissions. An unreadable, invalid or
unsupported saved setting falls back to English. If a change cannot be saved,
the menu reports the failure and keeps the previous language.

Prompts, progress/error messages, built-in fallback text and PDF report labels
come from [English](locales/en.json) and [Spanish](locales/es.json) catalogues.
Country/carrier descriptions use the selected language where the phone metadata
library supports it. Text returned by external services is not automatically
translated. JSON field names remain stable; `metadata.language` records the
language used for the report.

To add a language, copy `locales/en.json` to a new language-code file, set its
`language_name`, and translate the message values. Keep the message keys and
format placeholders such as `{language}` and `{v0}` unchanged. The menu discovers
catalogue files automatically. Missing translations fall back to English.
The current PDF font supports English and Spanish; languages needing other
scripts also require an appropriate Unicode font before PDF export is supported.

Offline checks (with the existing requirements installed):

```bash
python -m unittest discover -s tests -v
```

Tests use temporary preferences, synthetic numbers and blocked API calls. PDF
label extraction is additionally checked when `fpdf2` and `pdftotext` are present.
