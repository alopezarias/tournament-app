from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.goal import GoalCreate, GoalOut
from app.services import goal_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[GoalOut])
def read_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return goal_service.get_goals(db, skip=skip, limit=limit)

@router.post("/", response_model=GoalOut)
def create_new_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    return goal_service.create_goal(db, goal)

@router.delete("/{goal_id}", response_model=GoalOut)
def delete_existing_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = goal_service.delete_goal(db, goal_id)
    if not db_goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return db_goal
