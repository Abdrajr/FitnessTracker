from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WorkoutBase(BaseModel):
    activity_type: str 
    duration: int
    calories_burned: int

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(BaseModel):
    activity_type: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[int] = None
    
class WorkoutResponse(WorkoutBase):
    id: int
    date: datetime  

    class Config:
        from_attributes = True

class WorkoutListResponse(BaseModel):
    data: List[WorkoutResponse]
