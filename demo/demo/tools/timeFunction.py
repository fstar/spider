from datetime import datetime


def get_current_day():
    t = datetime.now()
    day = t.strftime("%Y-%m-%d")
    return day


def get_current_time():
    t = datetime.now()
    t = t.strftime("%H:%M:%S")
    return t


def get_current_day_time():
    t = datetime.now()
    one = {}
    one["dealtime_day"] = t.strftime("%Y-%m-%d")
    one["dealtime_time"] = t.strftime("%H:%M:%S")
    return one