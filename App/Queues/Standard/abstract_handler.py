from abc import ABC, abstractmethod
from importlib import import_module


class AbstractHandler(ABC):
    __next_handler = None

    @abstractmethod
    def get_steps(self) -> list:
        pass

    @abstractmethod
    def get_namespace(self) -> str:
        pass

    def init(self):
        self.handle()
        return self

    def handle(self) -> bool:
        self.set_next()
        if not self.has_finished():
            self.__next_handler.handle()
        return True

    def set_next(self):
        self.__next_handler = self.get_step()

    def get_step(self):
        step = self.get_next_step()

        if step == '':
            return None

        step_module = self.get_step_module(step)
        class_name = self.get_step_class_name(step)
        step_class = getattr(step_module, class_name)
        return step_class()

    def get_next_step(self):
        current_module = self.__class__.__module__
        current_step = current_module.split('.').pop()
        step_index = self.get_next_step_index(current_step)

        if step_index == -1:
            return ''

        return self.get_steps()[step_index]

    def get_next_step_index(self, current_step: str):
        steps = self.get_steps()

        try:
            index = steps.index(current_step) + 1
        except ValueError:
            return 0

        if index == len(steps):
            return -1

        return index

    def get_step_module(self, step: str):
        module_namespace = f'{self.get_base_namespace()}.{step}'
        return import_module(module_namespace)

    def get_base_namespace(self):
        return f'App.Queues.{self.get_namespace()}.Steps'

    def get_step_class_name(self, step: str):
        name_parts = step.split('_')
        return ''.join([name.capitalize() for name in name_parts])

    def has_finished(self):
        return self.__next_handler is None
