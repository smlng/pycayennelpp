from datetime import datetime
from datetime import timezone as tz


def datetime_as_utc(dt):
    """Helper function necessary for pyton <=3.5
    to convert naive datetime to utc"""
    try:
        # works with naive datetime object in python 3.6+
        return dt.astimezone(tz.utc)
    except ValueError:
        # necessary in python <= 3.5
        pass
    if dt.tzinfo is None:
        now = datetime.now().replace(microsecond=0, second=0)
        utcnow = datetime.utcnow().replace(microsecond=0, second=0)
        localtz = tz(now - utcnow)
        dt = datetime.fromtimestamp(dt.timestamp(), localtz)
    return dt.astimezone(tz.utc)
