"""Utility functions for the API."""
from typing import Dict, Any
from uuid import UUID


def convert_uuids_to_strings(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert all UUID values in a dictionary to strings for JSON serialization."""
    result = {}
    for key, value in data.items():
        if isinstance(value, UUID):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = convert_uuids_to_strings(value)
        elif isinstance(value, list):
            result[key] = [
                convert_uuids_to_strings(item) if isinstance(item, dict) else
                str(item) if isinstance(item, UUID) else item
                for item in value
            ]
        else:
            result[key] = value
    return result

