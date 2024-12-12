import asyncio
import logging
from asyncio import sleep
from typing import Optional

from app.task.base import BaseTask


class Task(BaseTask):
    """Task implementation with self-managed execution"""
    def __init__(self, duration: int):
        super().__init__()
        self.duration = duration
        self.current_time = duration
        self._execution_task: Optional[asyncio.Task] = None
    
    async def _execute(self):
        """Internal execution method"""
        try:
            logging.info(f"Starting task execution, duration: {self.duration}")
            start_time = asyncio.get_event_loop().time()
            
            # not for loop, because time is tracked more accurately with while
            while self.current_time > 0:
                await sleep(1)
                elapsed = int(asyncio.get_event_loop().time() - start_time)
                self.current_time = max(0, self.duration - elapsed)
                logging.info(f"Task progress: {self.current_time} seconds remaining")
            
            self._is_completed = True
            logging.info("Task completed")
        except asyncio.CancelledError:
            logging.info("Task cancelled")
            raise
        except Exception as e:
            logging.error(f"Error executing task: {e}", exc_info=True)
            raise
    
    async def start_completing(self):
        """Start task execution in background"""
        if not self._execution_task:
            self._execution_task = asyncio.create_task(self._execute())
            await asyncio.sleep(0)

            if not self._execution_task.done():
                logging.info("Task started successfully")
            else:
                logging.error("Task failed to start")
                if self._execution_task.exception():
                    raise self._execution_task.exception()
    
    def get_remaining_time(self) -> int:
        return self.current_time
