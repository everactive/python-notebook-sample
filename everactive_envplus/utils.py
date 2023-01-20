from typing import Iterable, Optional


def coalesce(values: Iterable[Optional[str]]) -> Optional[str]:
    """Return the first non-None value or None if all values are None."""
    return next((v for v in values if (v is not None) and (v != "")), None)