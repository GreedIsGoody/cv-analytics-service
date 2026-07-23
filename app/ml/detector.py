import os
from pathlib import Path 
import cv2 
from ultralytics import YOLO

class VehicleDetector:
    #Identificators
    VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
    
    def __init__(self, model_name: str = "yolov8n.pt"):
        pass