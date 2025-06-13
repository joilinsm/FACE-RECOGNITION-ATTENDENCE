import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
from datetime import datetime
import requests

# === CONFIG ===
known_faces_dir = "known_faces"
csv_filename = "attendance.csv"

# === Load Known Faces ===
known_face_encodings = []
known_face_names = []

print("[INFO] Loading known faces...")
for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0].upper())
        else:
            print(f"⚠️ No face found in {filename}")
print(f"[INFO] Loaded {len(known_face_encodings)} known faces.")

# === Location Function ===
def get_location():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5)
        data = res.json()
        return f"{data.get('city')}, {data.get('region')}, {data.get('country')} (Lat/Lon: {data.get('loc')})"
    except:
        return "Unknown"

# === Attendance Function ===
def mark_attendance(name):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    location = get_location()

    df = pd.DataFrame([[name, dt_string, location]], columns=["Name", "Time", "Location"])
    if not os.path.isfile(csv_filename):
        df.to_csv(csv_filename, index=False)
    else:
        df.to_csv(csv_filename, mode='a', header=False, index=False)

    print(f"✅ Marked: {name} at {dt_string} | Location: {location}")

# === Start Webcam ===
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
process_this_frame = True

print("[INFO] Starting video stream. Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Skip alternate frames for speed
    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                mark_attendance(name)

                # Scale back face locations
                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    process_this_frame = not process_this_frame

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
cap.release()
cv2.destroyAllWindows()
print(f"✅ Attendance logging stopped. Data saved to '{csv_filename}'")
