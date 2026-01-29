import cv2
import face_recognition
import database
import numpy as np
import time

class AttendanceSystem:
    def __init__(self):
        self.cap = None
        self.known_face_encodings = []
        self.known_face_ids = []
        self.known_face_names = []
        
        # Logic state
        self.REQUIRED_CONSECUTIVE_FRAMES = 6 
        self.current_match_count = {} 
        self.last_message = "Ready to Mark Attendance"
        self.message_time = time.time()
        self.display_duration = 3
        
        self.mode = 'in' # Default mode, can be 'in' or 'out'

    def set_mode(self, mode):
        self.mode = mode
        self.last_message = f"Mode: Punch {mode.upper()}"
        self.message_time = time.time()

    def load_users(self):
        users = database.get_all_users()
        self.known_face_encodings = []
        self.known_face_ids = []
        self.known_face_names = []

        for user in users:
            encoding = np.array(user["face_encoding"])
            self.known_face_encodings.append(encoding)
            self.known_face_ids.append(user["user_id"])
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

        # Resize for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        seen_user_ids = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            user_id = None
            
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    user_id = self.known_face_ids[best_match_index]

            if user_id:
                seen_user_ids.append(user_id)
                count = self.current_match_count.get(user_id, 0) + 1
                self.current_match_count[user_id] = count
                
                if count == self.REQUIRED_CONSECUTIVE_FRAMES:
                    # Pass the current mode to database
                    result_msg = database.mark_attendance(user_id, action=self.mode)
                    if result_msg:
                        self.last_message = result_msg
                        self.message_time = time.time()
            else:
                pass

        # Reset counters
        for uid in list(self.current_match_count.keys()):
            if uid not in seen_user_ids:
                self.current_match_count[uid] = 0

        # Draw Message
        if time.time() - self.message_time < self.display_duration:
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 50), (50, 50, 50), cv2.FILLED)
            cv2.putText(frame, self.last_message, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            mode_text = f"Scanning ({self.mode.upper()})..."
            cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        # Draw boxes
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

attendance_system = AttendanceSystem()

def start_attendance():
    print("Please use the web interface.")

