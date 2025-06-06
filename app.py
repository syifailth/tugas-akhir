import cv2
import os
from flask import Flask, render_template, Response, request, jsonify
from datetime import datetime
from utils.yolov8_detector import YOLOv8Detector

app = Flask(__name__)

# Folder penyimpanan gambar
IMAGE_FOLDER = "static/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Inisialisasi YOLOv8
model_path = "yolov8_model/best.pt"
detector = YOLOv8Detector(model_path)

camera = None
camera_active = False 

# Warna untuk bounding box
CLASS_COLORS = {
    "Healthy": (0, 255, 0),  
    "Early Blight": (0, 0, 255),  
    "Late Blight": (255, 0, 0),  
    "Leaf Mold": (255, 165, 0),  
    "Septoria": (128, 0, 128)  
}

def generate_frames():
    global camera
    while camera_active:
        if camera is None or not camera.isOpened():
            break

        success, frame = camera.read()
        if not success:
            break
        else:            
            detected_frame = detector.detect(frame, class_colors=CLASS_COLORS)
            ret, buffer = cv2.imencode('.jpg', detected_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera, camera_active
    if camera is None or not camera_active:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            return jsonify({"status": "failed", "message": "Camera not available"})
        camera_active = True
    return jsonify({"status": "started"})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera, camera_active
    if camera is not None and camera_active:
        camera_active = False
        camera.release()
        camera = None
    return jsonify({"status": "stopped"})

@app.route('/capture', methods=['POST'])
def capture():
    global camera
    if camera is not None and camera_active:
        success, frame = camera.read()
        if success:            
            detected_frame = detector.detect(frame, class_colors=CLASS_COLORS)
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(IMAGE_FOLDER, filename)
            cv2.imwrite(filepath, detected_frame)
            return jsonify({"status": "saved", "image_url": f"/{filepath}"})
    return jsonify({"status": "failed"})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
