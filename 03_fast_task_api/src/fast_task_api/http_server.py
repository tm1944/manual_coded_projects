from uuid import UUID
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel, Field
from fast_task_api.task import Task, TaskNotFoundError, TaskService,TaskStorage

app = FastAPI()
task_storage = TaskStorage()


def get_service():
	return TaskService(TaskStorage)

class CreateTaskRequest(BaseModel):
    name: str = Field(min_length=1)


class UpdateTaskRequest(BaseModel):
    completed: bool


def task_or_404(task_id: UUID) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} was not found.",
    )


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(request: CreateTaskRequest, task_service = Depends(get_service)) -> Task:
    return task_service.create_task(request.name)


@app.get("/tasks", response_model=list[Task])
def get_tasks(task_service = Depends(get_service)) -> list[Task]:
    return task_service.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID, task_service = Depends(get_service)) -> Task:
    try:
        return task_service.get_task(task_id)
    except TaskNotFoundError:
        raise task_or_404(task_id) from None


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, request: UpdateTaskRequest, task_service = Depends(get_service)) -> Task:
    try:
        return task_service.set_task_completion(task_id, request.completed)
    except TaskNotFoundError:
        raise task_or_404(task_id) from None


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, task_service = Depends(get_service)) -> Response:
    try:
        task_service.delete_task(task_id)
    except TaskNotFoundError:
        raise task_or_404(task_id) from None

    return Response(status_code=status.HTTP_204_NO_CONTENT)
