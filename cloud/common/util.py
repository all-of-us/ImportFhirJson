import datetime
from typing import Optional

import chrono


def value_or_default(src: dict, key: str, default):
    """
    value_or_default attempts to locate a value within a dict, returning the provided default should it not be found

    :param src: source dictionary
    :param key: dictionary key name
    :param default: value to return should the key not be found in the src dict
    :return:
    """
    if key in src:
        return src[key]
    else:
        return default


def datetime_or_none(src: dict, key: str) -> Optional[datetime.datetime]:
    """
    datetime_or_none attempts to locate and parse an RFC3339 datetime value from a dictionary, returning None if the
    key is not found in the provided dict

    :param src: source dictionary
    :param key: key containing RFC3339 datetime value
    :return:
    """
    if key in src:
        return chrono.then(src[key])
    else:
        return None
