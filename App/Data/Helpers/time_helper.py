import os
from datetime import datetime, time
from time import tzset

from pytz import timezone

hour_format = '%H:%M'
datetime_format = '%Y-%m-%d %H:%M:%S.%f'


def treat_string_hour_to_time(str_time: str):
    base_time = str_time.split(':')
    hour = int(base_time[0])
    minute = int(base_time[1])
    return time(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
        tzinfo=timezone('America/Sao_Paulo')
    )


def treat_datetime_to_string_hour(date: datetime):
    return date.strftime(hour_format)


def set_time_zone():
    os.environ['TZ'] = 'America/Sao_Paulo'
    tzset()
