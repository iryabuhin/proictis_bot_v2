from abc import ABC, abstractmethod
from typing import Optional, AnyStr, List, Dict, Union


class Handler(ABC):

    @abstractmethod
    def link_with(self, handler):
        pass

    @abstractmethod
    def handle(self, response: Dict) -> Dict:
        pass


class AbstractHandler(Handler):

    _next_handler: Handler = None

    def link_with(self, handler: Handler) -> Handler:
        self._next_handler = handler

    def handle(self, response: Dict) -> Dict:
        if self._next_handler is not None:
            self._next_handler.handle(response)

