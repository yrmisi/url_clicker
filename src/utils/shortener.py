import secrets
import string

from config import settings

ALNUM: str = string.ascii_letters + string.digits


def generate_slug():
    """Generate a random alphanumeric slug of the given length."""
    return "".join(secrets.choice(ALNUM) for _ in range(settings.app.slug_length))
