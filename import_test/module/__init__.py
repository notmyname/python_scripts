import os

env = os.environ.get('ENV','dev').lower()

if env == 'prod':
    from _prod import *
elif env == 'model':
    from _model import *
else:
    from _dev import *
