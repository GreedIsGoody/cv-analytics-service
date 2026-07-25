import shutil 
from pathlib import Path 
from typing import List 

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select 
from sqlalchemy.orm import selectinload 

from database import engine, Base, get_db 
from models import DetectionTask, DetectedObject
from app.schemas import DetectionTaskResponse 
from ml.detector import VehicleDetector

app = FastAPI(title="CV Analytics Service", version="1.0.0")

detector = VehicleDetector()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)