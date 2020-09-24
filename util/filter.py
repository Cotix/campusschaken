import pytz
from pytz import timezone
import tzlocal

from config import app


def datetimefmt(value, format="%m/%d/%y %I:%M"):
    tz = pytz.timezone('Europe/Amsterdam')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

app.jinja_env.filters['datetimefmt'] = datetimefmt