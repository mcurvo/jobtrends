# utils/location.py

import re
from geotext import GeoText

# Keywords indicating remote work
REMOTE_KEYWORDS = {'remote', 'work from home', 'distributed'}

def parse_and_normalize(location_field):
    """
    Extract city names from a raw location string using GeoText,
    detect 'Remote' mentions, and return a list of normalized names.
    """
    if not isinstance(location_field, str):
        return []
    # Standardize separators
    text = location_field.replace('/', ', ')
    # Extract recognized city names
    cities = GeoText(text).cities
    # Detect remote work
    if any(kw in text.lower() for kw in REMOTE_KEYWORDS):
        cities.append('Remote')
    # Title-case and dedupe
    normalized = []
    for city in cities:
        c = city.title()
        if c not in normalized:
            normalized.append(c)
    return normalized
