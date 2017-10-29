'''
Teach JSON how to seralise Types.
'''
from json_default import default

from . import Type


@default.register(Type)
def _(obj):
    return obj.__json__()
