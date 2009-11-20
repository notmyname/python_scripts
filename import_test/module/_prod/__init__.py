import os

def _load_events():
    parent_dir = os.path.dirname(__file__)
    base = os.path.basename(os.path.dirname(parent_dir))
    modules = []
    for root, dirs, files in os.walk(parent_dir):
        for name in files:
            if name.endswith('.py') and not name.startswith('__') and not name.startswith('.'):
                module_name = '%s.%s.%s' % (base, os.path.basename(parent_dir), name.rsplit('.', 1)[0].replace(os.sep, '.'))
                __import__(module_name)
                modules.append(module_name)
    return modules

__all__ = []

def update__all__():
    global __all__
    __all__ = [x.rsplit('.',1)[-1] for x in _load_events()]

update__all__() # intial setup
