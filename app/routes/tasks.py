from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create task
@router.post("/", response_model=TaskResponse)
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
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    
    return tasks

# Update task (fixing the original logic which was incorrectly deleting the task)
@router.put("/{task_id}", response_model=TaskResponse)
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

    # Update the fields only if they are provided (i.e., not None)
    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.completed is not None:
        db_task.completed = task.completed

    # Commit the changes to the database
    db.commit()
    db.refresh(db_task)

    return db_task
