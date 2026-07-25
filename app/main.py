import shutil 
from pathlib import Path 
from typing import List, Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload 

from app.database import engine, Base, get_db 
from app.models import DetectionTask, DetectedObject
from app.schemas import DetectionTaskResponse 
from app.ml.detector import VehicleDetector

# Context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        yield     
        await engine.dispose()
        
#initialize our app
app = FastAPI(title="CV Analytics Service", version="1.0.0", lifespan=lifespan)

#Init model
detector = VehicleDetector()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Receiving a picture - give it to ai(YOLO) - record result in postgres - in json
@app.post("/api/v1/detect", response_model=DetectionTaskResponse, status_code=status.HTTP_201_CREATED)
async def process_image(
    file: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File need to be a image")
    
    #Record file on disk
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    #ML inference    
    try:
        detection_result = detector.detect_vehicles(str(file_location))
        
        detector.save_annotated_image(detection_result, str(file_location))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error of ML-interface: {str(e)}")
    
    #Adding in Postgres
    task = DetectionTask(
        filename = file.filename,
        total_vehicles=detection_result["total_vehicles"],
        counts=detection_result["counts"]
    )
    db.add(task)
    await db.flush()
    
    for obj in detection_result["detections"]:
        detected_obj = DetectedObject(
            task_id = task.id,
            object_class= obj["class"],
            confidence=obj["confidence"],
            bbox=obj["bbox"]
        )
        
        db.add(detected_obj)
        
    await db.commit()
    #
    query = select(DetectionTask).options(selectinload(DetectionTask.objects)).where(DetectionTask.id == task.id)
    result = await db.execute(query)
    saved_task  = result.scalar_one()
    
    return saved_task

@app.get("/api/v1/tasks", response_model=List[DetectionTaskResponse])
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    query = select(DetectionTask).options(selectinload(DetectionTask.objects))
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


@app.get("/api/v1/tasks/{task_id}/image", response_class=FileResponse)
async def get_task_image(task_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(DetectionTask).where(DetectionTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    #Checking if task exists
    if not task:
        raise HTTPException(status_code=404, detail= "Task was not found")
    
    file_path = UPLOAD_DIR / task.filename
    
    #Checking if image exists
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found on disk")
    
    return FileResponse(path=file_path, media_type="image/jpeg", filename=task.filename)


@app.get("/api/v1/tasks/tasks/recent", response_model=List[DetectionTaskResponse])
async def get_recent_tasks(db: Annotated[AsyncSession, Depends(get_db)]):
    
    query = select(DetectionTask).options(selectinload(DetectionTask.objects)).order_by(desc(DetectionTask.created_at)).limit(3)
    
    result = await db.execute(query)
    
    tasks = result.scalars().all()
    
    return tasks