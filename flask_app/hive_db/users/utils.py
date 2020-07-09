import datetime as det

def get_now():
    return det.datetime.now()

def get_now_minus_timedelta(days=0, mins=0, hours=0):
    return get_now() - det.timedelta(days=days, minutes=mins, hours=hours)


if __name__ == "__main__":
    now = get_now()
    print(now)
    now_minus_1_week = get_now_minus_timedelta(days=7)