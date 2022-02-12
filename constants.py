import datetime


CACHE_DICT = [
  'today', 
  'tomorrow',
  'day-after-tomorrow'
]

TIME_DELTA_MAP = {
  'today':0, 
  'tomorrow': 1, 
  'day-after-tomorrow': 2
}

DATE_FORMAT = "%H:%M:%S"
TIME_MIDNIGHT = str(datetime.time(23,59,59))
