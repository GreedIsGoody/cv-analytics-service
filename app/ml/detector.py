import os
from pathlib import Path
import cv2
from ultralytics import YOLO


class VehicleDetector:
    
    VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

    def __init__(self, model_name: str = "yolov8n.pt"):
        
        print(f"Loading a model {model_name}...")
        self.model = YOLO(model_name)

    def detect_vehicles(self, image_path: str, conf_threshold: float = 0.35) -> dict:
        
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл {image_path} не найден!")

        
        results = self.model(image_path, conf=conf_threshold)[0]

        detections = []
        counts = {"car": 0, "motorcycle": 0, "bus": 0, "truck": 0}

        
        if results.boxes is not None:
            for box in results.boxes:
                cls_id = int(box.cls[0].item())

                
                if cls_id in self.VEHICLE_CLASSES:
                    label_name = self.VEHICLE_CLASSES[cls_id]
                    confidence = round(float(box.conf[0].item()), 2)
                    
                    
                    bbox = [round(coord, 1) for coord in box.xyxy[0].tolist()]

                    counts[label_name] += 1
                    detections.append({
                        "class": label_name,
                        "confidence": confidence,
                        "bbox": bbox
                    })

        return {
            "total_vehicles": sum(counts.values()),
            "counts": counts,
            "detections": detections,
            "raw_results": results  
        }

    def save_annotated_image(self, results_dict: dict, output_path: str) -> str:
        
        raw_results = results_dict["raw_results"]
        
        
        annotated_frame = raw_results.plot()

       
        cv2.imwrite(output_path, annotated_frame)
        print(f"Annotated image saved: {output_path}")
        return output_path



def run_test():
    base_dir = Path(__file__).resolve().parent.parent
    test_img = os.path.join(base_dir, "test_image.jpg")
    output_img = os.path.join(base_dir, "result_image.jpg")

    print(f"Find a test image: {test_img}")
    if not os.path.exists(test_img):
        print(f"⚠️ Error, put image in directory {base_dir}")
        return

    detector = VehicleDetector(model_name="yolov8n.pt")
    
    print("\nAnalys picture..")
    results = detector.detect_vehicles(test_img)

    print("\n--- Result of detection ---")
    print(f"All transport: {results['total_vehicles']}")
    print(f"By types: {results['counts']}")
    print(f"First 3: {results['detections'][:3]}")

    detector.save_annotated_image(results, output_img)


if __name__ == "__main__":
    run_test()