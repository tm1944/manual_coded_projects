from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Task(BaseModel):
    """A task as the application stores and returns it."""

    uuid: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1)
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TaskNotFoundError(Exception):
    """Raised when a task ID is not in storage."""

class TaskStorage:
    """In-memory persistence for tasks."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def save(self, task: Task) -> Task:
        self._tasks[task.uuid] = task
        return task

    def find_all(self) -> list[Task]:
        return list(self._tasks.values())

    def find_by_id(self, task_id: UUID) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as error:
            raise TaskNotFoundError(task_id) from error

    def delete(self, task_id: UUID) -> None:
        self.find_by_id(task_id)
        del self._tasks[task_id]


class TaskService:
    """Task use cases and business rules."""

    def __init__(self, storage: TaskStorage | None = None) -> None:
        self._storage = storage or TaskStorage()

    def create_task(self, name: str) -> Task:
        return self._storage.save(Task(name=name))

    def get_all_tasks(self) -> list[Task]:
        return self._storage.find_all()

    def get_task(self, task_id: UUID) -> Task:
        return self._storage.find_by_id(task_id)

    def set_task_completion(self, task_id: UUID, completed: bool) -> Task:
        task = self._storage.find_by_id(task_id)
        task.status = "completed" if completed else "pending"
        return self._storage.save(task)

    def delete_task(self, task_id: UUID) -> None:
        self._storage.delete(task_id)
