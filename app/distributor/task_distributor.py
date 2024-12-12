from app.distributor.base import BaseDistributor
from app.node.base import BaseNode
from app.task.task import Task


class TaskDistributor(BaseDistributor):
    def __init__(self):
        super().__init__()

    def _get_best_node(self) -> BaseNode:
        """Get node with minimum total execution time"""
        return min(self.nodes, key=lambda n: n.get_metric())

    async def distribute_task(self, task: Task):
        """Distribute task to the best available node"""
        if not self.nodes:
            raise RuntimeError("No nodes registered in the system")
        
        best_node = self._get_best_node()
        await best_node.register_task(task)

