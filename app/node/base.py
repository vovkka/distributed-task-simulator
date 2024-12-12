from abc import ABC, abstractmethod

from app.task.task import Task


class BaseNode(ABC):
    @abstractmethod
    def __init__(self):
        self.current_task: Task | None = None
        self.is_executing = False

    @abstractmethod
    def run(self):
        ...

    def stop(self):
        self.is_executing = False

    @abstractmethod
    def register_task(self, task: Task):
        ...

    @abstractmethod
    def get_metric(self) -> int:
        """
        Describes the metric
        on the basis of which the distributor decides
        who to assign the task to
        """
        ...
