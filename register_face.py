import cv2
import face_recognition
import database
import numpy as np

class FaceRegister:
    def __init__(self):
        self.cap = None
        self.last_frame = None

    def start_camera(self):
        if self.cap is None or not self.cap.isOpened():
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
        
        self.last_frame = frame.copy() # Store for saving
        
        # Encode for web streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def save_face(self, user_id, name):
        """
        Saves the face from the last captured frame.
        """
        if self.last_frame is None:
            return False, "No frame captured yet."

        rgb_frame = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            return False, "No face detected."
        elif len(face_locations) > 1:
            return False, "Multiple faces detected."
        
        # Encode
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        encoding_list = face_encoding.tolist()
        
        # Save
        if database.add_user(user_id, name, encoding_list):
            return True, "User registered successfully!"
        else:
            return False, "User ID already exists."

# Global instance for simplicity in this demo
register_system = FaceRegister()

# Keep the old function for CLI compatibility (optional, or just remove)
def register(user_id=None, name=None):
    # This legacy function is now deprecated in favor of the web class
    print("Please use the web interface.")

