from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create task
@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=False,
        user_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# Get all tasks for the current user
@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    
    return tasks

# Update task (fixing the original logic which was incorrectly deleting the task)
@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    db_task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == user_id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the fields
    db_task.title = task.title if task.title else db_task.title
    db_task.description = task.description if task.description else db_task.description
    db_task.completed = task.completed if task.completed is not None else db_task.completed

    db.commit()
    db.refresh(db_task)

    return db_task
