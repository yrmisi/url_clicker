from .health import router as router_health
from .index import router as router_root
from .shortener import router as router_shortener

__all__ = [
    "router_root",
    "router_health",
    "router_shortener",
]
