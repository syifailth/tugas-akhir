import cv2
import torch
from ultralytics import YOLO

class YOLOv8Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame, class_colors):
        results = self.model(frame)
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls]
                
                # Pilih warna berdasarkan kelas
                color = class_colors.get(label, (255, 255, 255))  # Default putih
                
                # Gambar bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Tambahkan background warna pada label
                label_text = f"{label} ({conf:.2f})"
                (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y1 - th - 5), (x1 + tw, y1), color, -1) # Background label
                cv2.putText(frame, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1) # Teks hitam
        
        return frame
