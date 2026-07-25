import uuid 
from datetime import datetime , timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base 

class DetectionTask(Base):
    __tablename__ = "detection_tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=True)
    total_vehicles = Column(Integer, default=0)
    counts = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    objects = relationship("DetectedObject", back_populates="task", cascade="all, delete-orphan")
    
    
class DetectedObject(Base):
    __tablename__ = "detected_objects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("detection_tasks.id", ondelete="CASCADE"), nullable=False)
    object_class = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    bbox = Column(JSON, nullable=False)
    
    task = relationship("DetectionTask", back_populates="objects")