import datetime

BIRTHDAY_DAY_LIST = [
    'today',
    'tomorrow',
    'day-after-tomorrow'
]

BIRTHDAY_CACHE_DICT = {
    'today' : 'birthday_today',
    'tomorrow' : 'birthday_tomorrow',
    'day-after-tomorrow' : 'birthday_day_after_tomorrow',
}

TIME_DELTA_MAP = {
    'today': 0,
    'tomorrow': 1,
    'day-after-tomorrow': 2
}

DATE_FORMAT = "%H:%M:%S"
TIME_MIDNIGHT = str(datetime.time(23, 59, 59))
