from abc import ABC, abstractmethod


class AbstractMessageCardBuilder(ABC):

    @property
    @abstractmethod
    def card(self) -> None:
        pass

    @abstractmethod
    def add_text(self) -> None:
        pass

    @abstractmethod
    def add_attachments(self) -> None:
        pass


