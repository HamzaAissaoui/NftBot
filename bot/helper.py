from datetime import datetime, timedelta

def diff_more_than_3_hours(date_1, date_2, hours_difference=3):
    if (date_1 - timedelta(hours=hours_difference)) >= date_2:
        return True
    return False