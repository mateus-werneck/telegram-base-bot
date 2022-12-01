from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from App.Data.Helpers.message_helper import back_icon
from App.Lib.Treat.list_treat import list_split


def treat_menu(menu: list, list_name: str, parts: int = 1):
    keyboard = list_split(menu, parts)
    
    for i, line in enumerate(keyboard):
        for j, option in enumerate(line):
            keyboard[i][j] = get_button(option)

    append_back_button(keyboard, list_name)
    return InlineKeyboardMarkup(keyboard)


def get_button(option: dict):
    return InlineKeyboardButton(
        text=option['name'], callback_data=option['id'])


def append_back_button(keyboard: list, type: str):
    keyboard.append([InlineKeyboardButton(
        f'{back_icon()} Voltar', callback_data=f'go_back_{type}')])
