from types import SimpleNamespace
from inspect import getmembers


class field:
    '''
    A descriptor for declaring fields on Types.
    '''
    def __init__(self, caster, default=None):
        self.caster = caster
        self.default = default
        self.name = None

    def __get__(self, instance, klass):
        if instance is None:
            return self
        return getattr(instance.__data, self.name, self.default)

    def __set__(self, instance, value):
        setattr(instance.__data, self.name, self.caster(value))


class MetaType(type):
    '''Quickly tell the fields their names.'''
    def __new__(mcs, name, bases, attrs):
        for name, attr in attrs.items():
            if isinstance(attr, field):
                attr.name = name
        return super().__new__(mcs, name, bases, attrs)


class Type(metaclass=MetaType):
    __slots__ = ()
    _field__data = None

    def __init__(self, data):
        self._field__data = SimpleNamespace()
        for key, value in data.items():
            setattr(self, key, value)

    def __json__(self):
        return {
            name: getattr(self, name)
            for name, prop in getmembers(self.__class__, lambda prop: isinstance(prop, field))
        }
