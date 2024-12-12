from abc import ABC, abstractmethod

from app.node.base import BaseNode
from app.task.task import Task


class BaseDistributor(ABC):
    """Base class, distributes task between nodes"""
    @abstractmethod
    def __init__(self):
        self.nodes: list[BaseNode] = []

    @abstractmethod
    def _get_best_node(self) -> BaseNode:
        ...

    @abstractmethod
    def distribute_task(self, task: Task):
        ...

    def register_node(self, nodes: list[BaseNode] | BaseNode):
        if isinstance(nodes, list):
            self.nodes.extend(nodes)
        else:
            self.nodes.append(nodes)



