from fastapi import FastAPI, status, HTTPException, Depends, Response
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.params import Body
from . import models, schemas
from datetime import date, datetime



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    


while True:

        try:
            conn = psycopg2.connect(host='localhost', database='fitness_tracker', user='postgres', password='240201jr',
                             cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('The Database connection was succesfull !')
            break
        except Exception as error:
            print('connecting to database failed')
            print("Error: ", error)
            time.sleep(2)


@app.get("/Test")
def test_workout(db: Session = Depends(get_db)):
     workouts = db.query(models.Workout).all()
     return workouts
      


      
 #  Retrieves a list of all workout records from the database.

@app.get("/workouts", response_model=schemas.WorkoutListResponse)
def get_workouts(db: Session = Depends(get_db)): 
    workouts = db.query(models.Workout).all()
    return {"data": workouts}





# Creates a new workout entry in the database.

@app.post("/workouts", status_code=status.HTTP_201_CREATED, response_model=schemas.WorkoutResponse)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):

    new_workout = models.Workout(**workout.dict())
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout
     
       
  
# Fetches a specific workout by its ID
     
@app.get("/workouts/{id}", response_model=schemas.WorkoutResponse)
def get_workout(id: int, db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()

    
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Workout with ID: {id} was not found")
        
    
    return workout



#  Updates an existing workout's details.

@app.put("/workouts/{id}", response_model=schemas.WorkoutResponse)
def update_workouts(id: int, workout: schemas.WorkoutUpdate, db: Session = Depends(get_db)):

    workout_query = db.query(models.Workout).filter(models.Workout.id == id)

    updated_workout = workout_query.first()
    
    if updated_workout == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Workout with id: {id} does not exist")
    filter_out_null_values = {}

    for k, v in workout.dict().items():
        if v != None:
            filter_out_null_values[k] = v
        
    workout_query.update(filter_out_null_values, synchronize_session=False)
    db.commit()
   
    return workout_query.first()



#  Deletes a workout by its ID.

@app.delete("/workouts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(id: int, db: Session = Depends(get_db)):

    workout = db.query(models.Workout).filter(models.Workout.id == id)
    
 

    if workout.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id: {id} does not exist")
    
    workout.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

