from calendar import timegm
from datetime import datetime, timezone


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts):
    return datetime.utcfromtimestamp(ts)
