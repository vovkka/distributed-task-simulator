from collections import deque as Deque

from app.task.task import Task


class TaskQueue:
    def __init__(self):
        self.total_time = 0
        self.deque: Deque[Task] = Deque()

    def add(self, task: Task):
        self.deque.append(task)
        self.total_time += task.current_time

    def pop(self) -> Task | None:
        if self.deque:
            popped_task = self.deque.popleft()
            self.total_time -= popped_task.current_time
            return popped_task
        return None

    def is_empty(self) -> bool:
        return len(self.deque) == 0
