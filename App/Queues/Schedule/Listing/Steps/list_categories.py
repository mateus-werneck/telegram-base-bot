from App.Data.Helpers.inline_keyboard_helper import treat_list_inline_keyboard
from App.Data.Helpers.message_helper import (MessageHelper, add_icon,
                                             open_book_icon)
from App.Lib.Bot.chat import BotChat
from App.Queues.Schedule.Listing.list_schedule_options import \
    ListScheduleOptions


class ListCategories(ListScheduleOptions):

    def handle(self) -> bool:
        title = self.get_text()
        schedule_options = self.get_categories()
        BotChat.instance().send_callback_query(schedule_options, title)
        return super().handle()

    def get_title(self):
        return f'Escolha uma categoria {MessageHelper.category_icon()}'

    def get_schedule_options(self):
        return treat_list_inline_keyboard(self.get_options())

    def get_options():
        return [
            {
                'id': 'create_schedule',
                'name': f'Cadastrar Novo Cronograma {add_icon()}'
            },
            {
                'id': 'show_schedule',
                'name': f'Visualizar Cronograma da Semana {open_book_icon()}'
            }
        ]
