from datetime import datetime, time, timedelta
from time import strptime

from pytz import timezone

iso_format = '%Y-%m-%dT%H:%M:%S.%fZ'
datetime_format = '%Y-%m-%d %H:%M:%S'
pt_br = '%d/%m/%Y'

def is_valid_pt_date(date: str):
    try:
        return strptime(date, pt_br) is not None
    except Exception:
        return False

def treat_iso_string_to_datetime(iso_string: str):
    time_obj = strptime(iso_string, iso_format)
    return datetime(
        year=(time_obj.tm_year),
        month=time_obj.tm_mon,
        day=time_obj.tm_mday,
        hour=time_obj.tm_hour,
        minute=time_obj.tm_min,
        second=0,
        microsecond=0,
        tzinfo=timezone('America/Sao_Paulo')
    )

def treat_date_string_to_datetime(date: str):
    return datetime.strptime(date, datetime_format)

def treat_datetime_to_iso_string(date: datetime):
    return datetime.strftime(date, datetime_format)

def treat_datetime_to_pt_date(date: datetime):
    return date.strftime(pt_br)

def get_datetime_minutes_before(date: datetime, minutes: float):
    return date - timedelta(minutes=minutes)

def get_datetime_minutes_after(date: datetime, minutes: float):
    return date + timedelta(minutes=minutes)

def add_time_to_date(date: datetime, time_obj: time):
    return date + timedelta(hours=time_obj.hour, minutes=time_obj.minute)

   
