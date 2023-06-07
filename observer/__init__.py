
from inspect import Parameter, Signature
from functools import partial


def make_signature(params):
    return Signature(Parameter(param, Parameter.POSITIONAL_OR_KEYWORD) for param in params)


class StructureMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        instance = super().__new__(cls, clsname, bases, clsdict)
        setattr(instance, "__signature__", make_signature(instance.__params__))
        return instance

class Structure(metaclass=StructureMeta):
    __params__ = []

    def __init__(self, *args, **kwargs) -> None:
        bound = self.__signature__.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            setattr(self, name, value)

subscribers = {}

class Notify(Structure):
    __params__ = ["event_type", "callback", "data"]


    def subscribe(self):
        subscribers[self.event_type] = partial(self.callback, data=self.data)
        return subscribers[self.event_type]

