from abc import ABC, abstractmethod
from typing import List

from app.distributor.task_distributor import TaskDistributor
from app.node.node import Node
from app.task.task import Task


class Command(ABC):
    """Base command interface"""
    @abstractmethod
    async def execute(self) -> str:
        pass


class AddTaskCommand(Command):
    """Command to add a new task"""
    def __init__(self, distributor: TaskDistributor, duration: int):
        self.distributor = distributor
        self.task = Task(duration)

    async def execute(self) -> str:
        await self.distributor.distribute_task(self.task)
        return f"Задание с длительностью {self.task.duration} секунд добавлено в систему"


class ShowStatusCommand(Command):
    """Command to show system status"""
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    async def execute(self) -> str:
        status = ["Состояние серверов:"]
        
        for node in self.nodes:
            if node.current_task:
                remaining = node.current_task.get_remaining_time()
                if node.current_task.is_completed:
                    status.append(f"Сервер {node.id}: пусто (задание завершено)")
                else:
                    status.append(f"Сервер {node.id}: выполняет задание (осталось {remaining} сек.)")
            else:
                status.append(f"Сервер {node.id}: пусто")
            
            if not node.task_queue.is_empty():
                queue_tasks = [str(task.duration) for task in node.task_queue.deque]
                status.append(f"    Очередь: [{', '.join(queue_tasks)} сек.]")
        
        return "\n".join(status)


class InitSystemCommand(Command):
    """Command to initialize the system"""
    def __init__(self, num_servers: int):
        self.num_servers = num_servers
        self.distributor = TaskDistributor()
        self.nodes: List[Node] = []

    async def execute(self) -> str:
        for i in range(self.num_servers):
            node = Node(i + 1)
            self.nodes.append(node)
            self.distributor.register_node(node)
        
        return f"Система инициализирована с {self.num_servers} серверами" 