from App.Data.Helpers.date_helper import (treat_datetime_to_pt_date,
                                          treat_iso_string_to_datetime)
from App.Data.Helpers.message_helper import alarm_clock
from App.Data.Helpers.time_helper import treat_datetime_to_string_hour


def treat_task_to_message(task: dict, grade: str):
    deadline = treat_iso_string_to_datetime(
        task.get('deadLine'))
    hour = treat_datetime_to_string_hour(deadline)
    due_date = treat_datetime_to_pt_date(deadline)
    return f'{alarm_clock()} Alerta de Tarefa.' \
        + f'\n<b>Turma: </b>{grade}' \
        + f'\n<b>Tarefa: </b>{task.get("name")}' \
        + f'\n<b>Descrição: </b>{task.get("description")}' \
        + f'\n<b>Data Limite: </b>{due_date}' \
        + f'\n<b>Horário de entrega: </b>{hour}'
