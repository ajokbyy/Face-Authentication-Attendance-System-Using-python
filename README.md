# Face Authentication Attendance System

A simple, Python-based system to mark attendance using facial recognition. It uses a real webcam, stores data in a local MongoDB database, and prevents duplicate markings.

## Features
- **Register Face**: Capture and store a user's face encoding.
- **Mark Attendance**: Recognize face, verify presence (anti-spoof), and log "Punch In" or "Punch Out".
- **Real-Time Recognition**: Fast recognition using OpenCV and face_recognition.
- **Local Database**: All data stored securely in MongoDB on your machine.

## Prerequisites
1.  **Python 3.8+** installed.
2.  **MongoDB** installed and running locally on default port (27017).
3.  **Webcam** connected.

## Installation

1.  **Install Required Libraries**:
    Open a terminal/command prompt and run:
    ```bash
    pip install opencv-python face_recognition pymongo numpy pandas
    ```
    *Note: `face_recognition` requires CMake and dlib. If you face errors on Windows, search for "install dlib python windows" for pre-built wheels.*

2.  **Start MongoDB**:
    Ensure your MongoDB service is running.

## How to Run

1.  Navigate to the project folder:
    ```bash
    cd new
    ```

2.  Run the main script:
    ```bash
    python main.py
    ```

## Usage Guide

### 1. Register New Face
- Select Option **1** in the menu.
- Enter a unique **User ID** (e.g., `101`) and **Name** (e.g., `Abhiraj`).
- Look at the camera.
- Press **'s'** to Save when your face is detected.
- Press **'q'** to Quit if needed.

### 2. Mark Attendance
- Select Option **2** in the menu.
- The camera will open.
- Stay still in front of the camera for a few seconds.
- Consider looking at the camera until you see **"Punch In"** or **"Punch Out"** message.
- The system requires ~6 consecutive frames of detection to confirm it's you (Anti-Spoof).

### 3. Test Recognition
- Select Option **3** to just see if the computer recognizes you without marking attendance.

## Project Structure
- `main.py`: The entry point menu.
- `database.py`: Handles MongoDB connection, adding users, and marking attendance.
- `register_face.py`: Logic for capturing and saving new faces.
- `attendance.py`: Main logic for the attendance loop.
- `recognize_face.py`: Simple visual test for recognition.

## Database Schema
- **Database**: `face_attendance_db`
- **Collection `users`**: `{user_id, name, face_encoding}`
- **Collection `attendance`**: `{user_id, date, punch_in_time, punch_out_time}`

## Limitations
- Lighting: Extreme backlighting may affect detection.
- Performance: Depends on CPU speed (embedding calculation is CPU intensive).
