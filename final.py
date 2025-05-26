import cv2
import face_recognition
import numpy as np
import mediapipe as mp
import speech_recognition as sr
import threading
from ultralytics import YOLO

# === Load known face ===
known_image = face_recognition.load_image_file(r"C:\Users\User\Desktop\Arya.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]
known_name = "Recognized User"

# === Load your custom trained YOLOv11 model ===
model = YOLO(r'C:\Users\User\Desktop\yolo\my_model\train\weights\best.pt')

# === Initialize MediaPipe FaceMesh ===
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# === Initialize Speech Recognizer ===
recognizer = sr.Recognizer()

def listen_speech():
    print("🎤 Voice system running. Speak anytime...\n")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"🗣 You said: {text}")
                except sr.UnknownValueError:
                    print("❌ Could not understand audio.")
                except sr.RequestError as e:
                    print(f"🔌 API Error: {e}")
        except Exception as e:
            print(f"⚠ Listening error: {e}")

# Start speech recognition thread
speech_thread = threading.Thread(target=listen_speech, daemon=True)
speech_thread.start()

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    original_frame = frame.copy()
    h, w, _ = original_frame.shape

    # === Face recognition ===
    rgb_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for encoding in face_encodings:
        matches = face_recognition.compare_faces([known_encoding], encoding)
        name = known_name if True in matches else "Unknown Person"
        face_names.append(name)

    # === Face mesh (orientation) ===
    frame_rgb = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
    results_mesh = face_mesh.process(frame_rgb)

    if results_mesh.multi_face_landmarks:
        for face_landmarks in results_mesh.multi_face_landmarks:
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            eye_diff = left_eye.x - right_eye.x

            direction = "Facing Center"
            if eye_diff > 0.08:
                direction = "Facing Left"
            elif eye_diff < -0.08:
                direction = "Facing Right"

            cv2.putText(original_frame, direction, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # === Draw face recognition results ===
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        color = (0, 255, 0) if name == known_name else (0, 0, 255)
        label = f"✅ {name}" if name == known_name else f"❌ {name}"
        cv2.rectangle(original_frame, (left, top), (right, bottom), color, 2)
        cv2.putText(original_frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # === YOLO object detection on the original frame ===
    results_yolo = model.predict(source=original_frame, conf=0.5, verbose=False)
    # results_yolo[0].plot() returns an annotated frame
    annotated_frame = results_yolo[0].plot()

    # === Overlay face recognition results on YOLO annotated frame ===
    # We'll combine by drawing face recognition rectangles and orientation on the YOLO output frame:
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        color = (0, 255, 0) if name == known_name else (0, 0, 255)
        label = f"✅ {name}" if name == known_name else f"❌ {name}"
        cv2.rectangle(annotated_frame, (left, top), (right, bottom), color, 2)
        cv2.putText(annotated_frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Draw orientation text as well
    if results_mesh.multi_face_landmarks:
        cv2.putText(annotated_frame, direction, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # === Display the combined frame ===
    cv2.imshow("YOLOv11 + Face Recognition + Speech System", annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
