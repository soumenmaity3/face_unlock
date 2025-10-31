import cv2
import numpy as np
import subprocess
import time
import os

def lock_laptop():
    """Lock Windows laptop"""
    subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])

# Load the trained model
model_path = "trained_model.yml"
if not os.path.exists(model_path):
    print("❌ Error: trained_model.yml not found!")
    input("Press Enter to exit...")
    exit()

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(model_path)

# Load face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start webcam
cap = cv2.VideoCapture(0)

print("🔒 Face Recognition Security Active...")
print("Looking for authorized user...")

# Recognition parameters
confidence_threshold = 70
recognition_count = 0
required_recognitions = 5
max_time = 10  # Try for 10 seconds
start_time = time.time()

unlocked = False

while (time.time() - start_time) < max_time:
    ret, frame = cap.read()
    
    if not ret or frame is None:
        time.sleep(0.03)
        continue
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))
        
        label, confidence = face_recognizer.predict(face_roi)
        
        if confidence < confidence_threshold and label == 1:
            recognition_count += 1
            print(f"✓ Recognized! Confidence: {int(confidence)} ({recognition_count}/{required_recognitions})")
            if recognition_count >= required_recognitions:
                print("✅ AUTHORIZED USER DETECTED!")
                unlocked = True
                break
        else:
            recognition_count = 0
    
    if unlocked:
        break
    
    time.sleep(0.05)

cap.release()

if unlocked:
    print("🔓 Access Granted - Welcome!")
    time.sleep(1)
else:
    print("❌ Unauthorized User or No Face Detected - Locking System in 3 seconds...")
    time.sleep(3)
    lock_laptop()