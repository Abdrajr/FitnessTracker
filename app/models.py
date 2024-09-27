from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, nullable=False )
    user_id = Column(Integer)
    activity_type = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    calories_burned = Column(Integer)
    date = Column(TIMESTAMP(timezone=True),
                  nullable=False, server_default=text('now()'))
                  