from pydantic import BaseModel
from typing import List, Dict 
from datetime import datetime 


class DetectedObjectSchema(BaseModel):
    object_class: str 
    confidence: float 
    bbox: List[float]
    
    class Config:
        from_attributes = True
        
        
class DetectionTaskResponse(BaseModel):
    id: str 
    filename: str
    total_vehicles: int
    counts: Dict[str, int]
    created_at: datetime 
    objects: List[DetectedObjectSchema] = []
    
    class Config:
        from_attributes = True