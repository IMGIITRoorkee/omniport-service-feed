import datetime
Cache_dict = {
  'today':'my_list_today', 
  'tomorrow': 'my_list_tom', 
  'day-after-tomorrow': 'my_list_dat' 
}

Delta_dict = {
  'today':0, 
  'tomorrow': 1, 
  'day-after-tomorrow': 2
}

Date_format = "%H:%M:%S"
Time_midnight = str(datetime.time(23,59,59))
