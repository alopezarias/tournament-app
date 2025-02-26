# backend/app/controllers/goal_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.goal import GoalCreate, GoalOut
from app.services.goal_service import get_goal, get_goals, create_goal, delete_goal
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[GoalOut])
def read_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_goals(db, skip, limit)

@router.post("/", response_model=GoalOut)
def create_new_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    return create_goal(db, goal)

@router.delete("/{goal_id}", response_model=GoalOut)
def delete_existing_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = delete_goal(db, goal_id)
    if not db_goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return db_goal
