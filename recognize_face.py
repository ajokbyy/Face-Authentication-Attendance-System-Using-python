import cv2
import face_recognition
import database
import numpy as np

class FaceRecognizer:
    def __init__(self):
        self.cap = None
        self.known_face_encodings = []
        self.known_face_names = []

    def load_users(self):
        users = database.get_all_users()
        self.known_face_encodings = []
        self.known_face_names = []

        for user in users:
            encoding = np.array(user["face_encoding"])
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(user["name"])
        print(f"Loaded {len(self.known_face_names)} users.")

    def start_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.load_users()
            self.cap = cv2.VideoCapture(0)

    def stop_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = None

    def get_frame(self):
        if not self.cap or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

recognizer_system = FaceRecognizer()

def recognize():
    print("Please use the web interface.")

