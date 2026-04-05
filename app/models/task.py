from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from app.database import Base

from datetime import datetime

class Task(Base):

 __tablename__ = "tasks"
 id = Column(Integer, primary_key=True, index=True)
 title = Column(String)
 description = Column(String)
 completed = Column(Boolean, default=False)

 created_at = Column(DateTime, default=datetime.utcnow)

 user_id = Column(Integer, ForeignKey("users.id"))
