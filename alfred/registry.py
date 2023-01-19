import __main__ as main_str
from typing import Union, List

from alfred.template.template import Template
from alfred.voter.voter import Voter


class Registry:
    _voter_registry, _template_registry = [], []

    def __init__(self):
        self._is_interactive = not hasattr(main_str, '__file__')

    def register(self, cls: Union[Voter, Template]):
        if isinstance(cls, Voter):
            self._voter_registry.append(cls)
        elif isinstance(cls, Template):
            self._template_registry.append(cls)
        else:
            raise TypeError("Only Voter or Template can be registered")

    def unregister(self, cls: Union[Voter, Template]):
        if isinstance(cls, Voter):
            self._voter_registry.remove(cls)
        elif isinstance(cls, Template):
            self._template_registry.remove(cls)
        else:
            raise TypeError("Only Voter or Template can be unregistered")

    @property
    def voters(self):
        return self._voter_registry

    @property
    def templates(self):
        return self._template_registry

_global_registry = Registry()

def register(cls: Union[Voter, Template]):
    _global_registry.register(cls)


def unregister(cls: Union[Voter, Template]):
    _global_registry.unregister(cls)


def voters() -> List[Voter]:
    return _global_registry.voters


def templates() -> List[Template]:
    return _global_registry.templates
