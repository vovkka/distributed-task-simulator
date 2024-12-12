from abc import ABC, abstractmethod


class BaseTask(ABC):
    @abstractmethod
    def __init__(self):
        self._is_completed = False

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    @abstractmethod
    def start_completing(self) -> bool:
        ...
