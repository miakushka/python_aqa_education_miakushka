import time
from datetime import datetime


# conver unixtimestamp to current UTC time
def ts_converter(timestamp):
    gmt = time.gmtime(timestamp)
    return time.strftime('%c', gmt)


print(ts_converter(1634389737))


# check if you need to go to Python courses today
def course_checker():
    current_day_number = datetime.today().weekday()
    current_day_string = datetime.today().strftime('%A')
    if current_day_number in (0, 3):
        print("GO and study! There is %s today!" % current_day_string)
    else:
        print("Take a rest, there is %s" % current_day_string)


course_checker()
