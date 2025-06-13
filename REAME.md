# 📸 Smart Face Recognition Attendance System


A real-time face recognition system that marks attendance with name, timestamp, and location using your webcam. Built with **Python**, **OpenCV**, and **face_recognition**.

---

## ✅ Features

- Detects and recognizes known faces from webcam
- Logs attendance with **name, time, and location**
- Saves to `attendance.csv`
- Automatically fetches **city & country** from your IP
- Lightweight & fast using the `hog` model

---

## create a virtual environment 
Syntax: python -m venv env

## Activate the environment
Syntax: .\env\Scripts\activate

## Requirements
pip install opencv-python face_recognition numpy pandas requests
or
pip install -r req.txt

## Run the project
Command: python recognition.py


