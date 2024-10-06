from flask import Flask, render_template, request, Response, redirect, url_for
import cv2
import numpy as np
import os
import time
from ultralytics import YOLO

app= Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"  # Folder to store uploaded videos
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route('/') 
def index(): 
	return render_template('index.html') 

@app.route('/display', methods=['POST'])
def display():
    if 'file' not in request.files:
        return "No file uploaded!", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file!", 400
    
    # Handle file (e.g., save it or process it)
    # For this example, just redirect to the index page
    return "File uploaded successfully!"  # Or redirect or render another template


def generate_framesv2(video_path, model_name):
    
    print("model : ",model_name)
    model = YOLO(model_name)
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run inference
        results = model(frame)
        
        # Extract and process bounding boxes
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                label = f"Accessible Vehicle: {confidence:.2f}"
                
                # Draw bounding box and label on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue  # Skip this frame if encoding fails

        # Yield the frame as a byte array for HTTP response
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # Release video capture
    cap.release()


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(url_for('index'))

    file = request.files['video']
    if file.filename == '':
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    model_name = request.form.get('model_name')  # Get selected model
   
    return redirect(url_for('video_feed', video_path=file_path,model_name=model_name))


@app.route('/video')
def video_feed():
    video_path = request.args.get("video_path")
    model_name = request.args.get("model_name")
    return Response(generate_framesv2(video_path,model_name=model_name), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')