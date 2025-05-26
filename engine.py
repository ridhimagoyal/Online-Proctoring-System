# detection/proctor_engine.py
import face_recognition
import cv2
import numpy as np
import mediapipe as mp
import speech_recognition as sr
import threading
import json
import time
from datetime import datetime
from ultralytics import YOLO

class ProctorEngine:
    def _init_(self):
        self.logs = []
        self.trust_score = 100

        # Load known face
        known_image = face_recognition.load_image_file(r"C:\\Users\\User\\Desktop\\Arya.jpg")
        self.known_encoding = face_recognition.face_encodings(known_image)[0]
        self.known_name = "Recognized User"

        # Load YOLOv11 model
        self.model = YOLO(r'C:\\Users\\User\\Desktop\\yolo\\my_model\\train\\weights\\best.pt')

        # MediaPipe FaceMesh
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

        # Speech recognizer
        self.recognizer = sr.Recognizer()

    def listen_speech(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5)
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.logs.append(self.create_violation('Common Noise is detected.'))
                    self.trust_score -= 5
                except:
                    pass
        except:
            pass

    def create_violation(self, vtype, duration=1):
        return {
            'type': vtype,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'duration': duration
        }

    def start_detection(self, duration=10):
        cap = cv2.VideoCapture(0)
        start_time = time.time()

        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Face Recognition
            for encoding in face_encodings:
                matches = face_recognition.compare_faces([self.known_encoding], encoding)
                if not True in matches:
                    self.logs.append(self.create_violation('Unknown Person'))
                    self.trust_score -= 10

            # Face Orientation
            results_mesh = self.face_mesh.process(rgb_frame)
            if results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    left_eye = face_landmarks.landmark[33]
                    right_eye = face_landmarks.landmark[263]
                    eye_diff = left_eye.x - right_eye.x
                    if eye_diff > 0.08:
                        self.logs.append(self.create_violation('Looking Left'))
                        self.trust_score -= 5
                    elif eye_diff < -0.08:
                        self.logs.append(self.create_violation('Looking Right'))
                        self.trust_score -= 5

            # YOLO Object Detection
            results_yolo = self.model.predict(source=frame, conf=0.5, verbose=False)
            for r in results_yolo:
                for cls in r.boxes.cls:
                    if int(cls) != 0:  # Not person
                        self.logs.append(self.create_violation('Other Object Detected'))
                        self.trust_score -= 5

            # Speech Detection (in a thread)
            speech_thread = threading.Thread(target=self.listen_speech)
            speech_thread.start()
            speech_thread.join(timeout=6)

        cap.release()
        cv2.destroyAllWindows()

        self.save_logs(self.logs)

        return {
            'trust_score': self.trust_score,
            'total_score': 90,
            'exam_status': 'Fail' if self.trust_score < 70 else 'Pass',
            'user': self.known_name
        }

    def save_logs(self, violations):
        with open('logs/violations.json', 'w') as f:
            json.dump(violations, f)

    def get_violation_logs(self):
        try:
            with open('logs/violations.json', 'r') as f:
                return json.load(f)
        except:
            return []
