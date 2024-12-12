from asyncio import sleep
import logging
from typing import Optional

from app.node.base import BaseNode
from app.task.task import Task
from app.task.task_queue import TaskQueue


class Node(BaseNode):
    """Node implementation with task execution and queue management"""
    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.task_queue = TaskQueue()
    
    def get_metric(self) -> int:
        """Calculate total execution time for all tasks"""
        current_task_time = self.current_task.get_remaining_time() if self.current_task else 0
        queue_time = self.task_queue.total_time
        logging.debug(f"Node {self.id} metric: current_task={current_task_time}, queue={queue_time}")
        return current_task_time + queue_time
    
    async def register_task(self, task: Task):
        logging.info(f"Node {self.id}: registering new task (duration: {task.duration})")
        if self.current_task is None:
            self.current_task = task
            await task.start_completing()
            return
        
        logging.info(f"Node {self.id}: adding task to queue (current queue time: {self.task_queue.total_time})")
        self.task_queue.add(task)
    
    async def run(self):
        """Main node execution loop"""
        self.is_executing = True
        logging.info(f"Node {self.id} started")
        
        while self.is_executing:
            try:
                if self.current_task:
                    if self.current_task.is_completed:
                        logging.info(f"Node {self.id}: current task completed")
                        self.current_task = None
                    else:
                        # give current task a chance to complete
                        await sleep(0.1)
                        continue
                
                # if no current task, check queue
                if not self.task_queue.is_empty():
                    next_task = self.task_queue.pop()
                    if next_task:
                        logging.info(f"Node {self.id}: starting new task from queue")
                        self.current_task = next_task
                        await self.current_task.start_completing()
                else:
                    # if no tasks, just wait
                    await sleep(0.1)
            
            except Exception as e:
                logging.error(f"Error in node {self.id}: {e}", exc_info=True)
                await sleep(1)





