# backend/app/services/goal_service.py
from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.schemas.goal import GoalCreate

def get_goal(db: Session, goal_id: int):
    return db.query(Goal).filter(Goal.id == goal_id).first()

def get_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Goal).offset(skip).limit(limit).all()

def create_goal(db: Session, goal: GoalCreate):
    db_goal = Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int):
    db_goal = get_goal(db, goal_id)
    if not db_goal:
        return None
    db.delete(db_goal)
    db.commit()
    return db_goal
