import os
from importlib import import_module


class Init:
    def __init__(self):
        self.namespace = 'App/Handlers'
        self.handlers = {}
        
        self.start()
    
    def start(self):    
        self.set_handlers()
        
        for class_name, namespace in self.handlers.items():
            module = import_module(namespace)
            handler = getattr(module, class_name)
            handler.instance()
        
    def set_handlers(self):
        if not os.path.exists(self.namespace):
            return
        
        for content in os.listdir(self.namespace):
            if content.find('pycache') != -1:
                continue
            content = f'{self.namespace}/{content}'
            self.handle_file(content)
        
    def handle_folder(self, content: str):
        if not os.path.isdir(content):
            return
        for sub_content in os.listdir(content):
            if content.find('pycache') != -1:
                continue
            sub_content = f'{content}/{sub_content}'
            self.handle_file(sub_content)
        
           
    def handle_file(self, content: str):        
        if not os.path.isfile(content):
            self.handle_folder(content)
            return

        module_name = content.replace('.py', '').replace('/', '.')
        class_name = self.get_class_name(module_name)
        self.handlers[class_name] = module_name

    def get_class_name(self, module_name:str):
        module = module_name.split('.').pop()
        return ''.join([name.capitalize() for name in module.split('_')])
