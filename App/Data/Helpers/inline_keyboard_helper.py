from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from App.Data.Helpers.message_helper import back_icon, delete_icon
from App.Lib.Treat.list_treat import list_split


def treat_menu(menu: list, menu_name: str, parts: int = 1):
    keyboard = list_split(menu, parts)

    for i, line in enumerate(keyboard):
        for j, option in enumerate(line):
            keyboard[i][j] = get_button(option, menu_name)

    return InlineKeyboardMarkup(keyboard)


def get_button(option: dict, menu_name: str):
    callback_data = f'{menu_name}_{option["id"]}'
    return InlineKeyboardButton(
        text=option['name'], callback_data=callback_data)


def append_back_button(keyboard: list):
    keyboard.append(
        {
            'id': f'go_back',
            'name': f'{back_icon()} Voltar'
        }
    )

def append_exit_button(keyboard: list):
    keyboard.append(
        {
            'id': f'exit',
            'name': f'{delete_icon()} Sair'
        }
    )
