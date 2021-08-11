import datetime

RFC3339_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def now() -> datetime.datetime:
    """
    _now returns now with a timestamp because thanks python.

    :return:
    """
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def now_str() -> str:
    """
    _now_str returns now as an rfc3339 string

    :return:
    """
    return now().strftime(RFC3339_FORMAT)


def then(rfc3339: str) -> datetime.datetime:
    """
    python is really good at time and does a good job and i'm not bitter at all.

    :param rfc3339: Raw RFC3339-formatted time string
    :return: timezone aware datetime instance.
    """
    return datetime.datetime.strptime(rfc3339, RFC3339_FORMAT).replace(tzinfo=datetime.timezone.utc)
