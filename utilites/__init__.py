import contextlib
import tzlocal
import datetime

from urllib.parse import urlencode
from urllib.request import urlopen


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')


def contains_sub(string, to_find, case=False):
    if case:
        if string.find(to_find) != -1:
            return True
        else:
            return False
    else:
        if string.lower().find(to_find.lower()) != -1:
            return True
        else:
            return False


def has_number(string):
    return any(char.isdigit() for char in string)


def unix_to_time(unix, ):
    unix_timestamp = float(unix)
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.datetime.fromtimestamp(unix_timestamp, local_timezone)
    if local_time.hour < 12:
        if local_time.hour < 10:
            return str(local_time)[len("2020-06-18") + 2:len(str(local_time)) - 6] + " AM"
        else:
            return str(local_time)[len("2020-06-18") + 2:len(str(local_time)) - 6] + " AM"
    miliTime = str(local_time)[len("2020-06-18") + 1:len(str(local_time)) - 6]
    miliTime = miliTime[:-3]
    hours, minutes = miliTime.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "AM"
    if hours > 12:
        setting = "PM"
        hours -= 12
    return f"{hours}:{minutes} " + setting


def from_timestamp(unix):
    return datetime.datetime.fromtimestamp(unix, tzlocal.get_localzone())


def current_time():
    return datetime.datetime.now()


def subtract_time(a, b):
    b = b.replace(tzinfo=None)
    return b - a



