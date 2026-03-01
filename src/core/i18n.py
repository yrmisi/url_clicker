import json
import os

from config.paths import LOCALES_DIR

translations_cache: dict[str, dict[str, str]] = {}


def load_translations_to_cache():
    """Loads translations into cache."""
    for lang_file in os.listdir(LOCALES_DIR):
        if lang_file.endswith(".json"):
            lang: str = lang_file[:-5]
            with open(LOCALES_DIR / f"{lang}.json", "r", encoding="utf-8") as f:
                translations_cache[lang] = json.load(f)
