from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent

ENVS_DIR: Path = BASE_DIR / "config" / "envs"

TEMPLATES_DIR: Path = BASE_DIR / "templates"

LOCALES_DIR: Path = BASE_DIR / "locales"
