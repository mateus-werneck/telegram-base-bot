from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from App.Data.Helpers.message_helper import back_icon, delete_icon
from App.Lib.Log.logger import Logger
from App.Lib.Treat.list_treat import list_split


def treat_keyboard(menu: list, menu_name: str, parts: int = 1):
    keyboard = list_split(menu, parts)

    for i, line in enumerate(keyboard):
        for j, option in enumerate(line):
            keyboard[i][j] = get_button(option, menu_name)

    return keyboard


def treat_menu(keyboard: list):
    return InlineKeyboardMarkup(keyboard)


def get_button(option: dict, menu_name: str):
    callback_data = f'{menu_name}_{option["id"]}'
    return InlineKeyboardButton(
        text=option['name'], callback_data=callback_data)


def append_back_button(keyboard: list, menu_name: str):
    button = {'id': f'go_back', 'name': f'{back_icon()} Voltar'}
    keyboard.append([get_button(button, menu_name)])


def append_exit_button(keyboard: list, menu_name: str):
    button = {'id': f'exit', 'name': f'{delete_icon()} Sair'}
    keyboard.append([get_button(button, menu_name)])


def append_custom_button(keyboard: list, menu_name: str,  id: str, name: str):
    button = {'id': id, 'name': name}
    keyboard.append([get_button(button, menu_name)])
