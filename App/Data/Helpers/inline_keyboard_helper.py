from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from App.Data.Helpers.message_helper import back_icon


def treat_list_inline_keyboard(options: list, list_name: str):
    keyboard = [options[i:i+1] for i in range(0, len(options), 1)]
    for i, line in enumerate(keyboard):
        for j, option in enumerate(line):
            keyboard[i][j] = InlineKeyboardButton(
                option['name'], callback_data=option['id'])
    append_back_button(keyboard, list_name)
    return InlineKeyboardMarkup(keyboard)

def append_back_button(keyboard: list, type: str):
    keyboard.append([InlineKeyboardButton(
        f'Voltar {back_icon()}', callback_data=f'go_back_{type}')])

