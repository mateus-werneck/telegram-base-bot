from importlib import import_module


class FactoryHandler:
    _handlers = {}

    @staticmethod
    def create(namespace: str):
        module = FactoryHandler.get_module(namespace)
        class_name = FactoryHandler.get_class_name(namespace)
        handler_class = getattr(module, class_name)

        FactoryHandler.delete_handler(class_name)
        FactoryHandler._handlers[class_name] = handler_class.instance()
        return FactoryHandler._handlers[class_name]

    @staticmethod
    def get_module(namespace: str):
        module_namespace = f'{FactoryHandler.get_base_namespace()}.{namespace}'
        return import_module(module_namespace)

    @staticmethod
    def get_base_namespace():
        return 'App.Handlers'

    @staticmethod
    def get_class_name(namespace: str):
        module_name = namespace.split('.').pop()
        name_parts = module_name.split('_')
        return ''.join([name.capitalize() for name in name_parts])

    @staticmethod
    def delete_handler(class_name: str):
        if FactoryHandler._handlers.get(class_name):
            del FactoryHandler._handlers[class_name]
