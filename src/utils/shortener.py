import secrets
import string

ALNUM: str = string.ascii_letters + string.digits


def generate_slug(length: int = 6):
    """Generate a random alphanumeric slug of the given length."""
    return "".join(secrets.choice(ALNUM) for _ in range(length))
