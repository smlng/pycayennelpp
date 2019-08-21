from datetime import datetime, timedelta
from datetime import timezone as tz

from cayennelpp.utils import datetime_as_utc


def test_datetime_as_utc():
    """Test converting naive datetime to utc datetime."""
    now = datetime.now().replace(microsecond=0, second=0)
    utcnow = datetime.now(tz.utc).replace(microsecond=0, second=0)
    assert datetime_as_utc(now) - utcnow <= timedelta(seconds=2)
