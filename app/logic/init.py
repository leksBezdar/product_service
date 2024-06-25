from functools import lru_cache
from punq import Container, Scope


from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator

from settings.settings import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    settings: Settings = container.resolve(Settings)  # noqa

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
