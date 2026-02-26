from dataclasses import dataclass


@dataclass
class SlugCountInfo:
    """Data with slug and its quantity."""

    slug: str
    creation_count: int
