from fastapi.templating import Jinja2Templates

from config.paths import TEMPLATES_DIR

templates = Jinja2Templates(directory=TEMPLATES_DIR)
