'''
Teach JSON how to seralise Types.
'''
from functools import partial
from json import dumps, loads
from json_default import default

from . import Type


@default.register(Type)
def _(obj):
    return obj.__json__()


dumps = partial(dumps, default=default)
