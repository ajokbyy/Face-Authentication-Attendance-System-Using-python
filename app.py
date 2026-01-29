from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import register_face
import attendance
import recognize_face
import database

app = Flask(__name__)

# --- Helper to manage cameras ---
def stop_all_cameras():
    register_face.register_system.stop_camera()
    attendance.attendance_system.stop_camera()
    recognize_face.recognizer_system.stop_camera()

def gen(camera_system):
    """Video streaming generator function."""
    camera_system.start_camera()
    while True:
        frame = camera_system.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# --- Routes ---

@app.route('/')
def home():
    stop_all_cameras()
    return render_template('index.html')

# --- Register ---
@app.route('/register_page')
def register_page():
    stop_all_cameras() # Stop others
    return render_template('register.html')

@app.route('/video_feed_register')
def video_feed_register():
    return Response(gen(register_face.register_system),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/register_save', methods=['POST'])
def register_save_api():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    
    if not user_id or not name:
        return jsonify({"success": False, "message": "Missing ID or Name"})
    
    success, msg = register_face.register_system.save_face(user_id, name)
    return jsonify({"success": success, "message": msg})


# --- Attendance ---
@app.route('/mark_attendance/in')
def mark_attendance_in():
    stop_all_cameras()
    attendance.attendance_system.set_mode('in')
    return render_template('attendance.html', title="Punch IN")

@app.route('/mark_attendance/out')
def mark_attendance_out():
    stop_all_cameras()
    attendance.attendance_system.set_mode('out')
    return render_template('attendance.html', title="Punch OUT")

@app.route('/video_feed_attendance')
def video_feed_attendance():
    return Response(gen(attendance.attendance_system),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Logs ---
@app.route('/attendance_logs')
def attendance_logs():
    stop_all_cameras()
    logs = database.get_attendance_logs()
    return render_template('logs.html', logs=logs)


# --- Recognize ---
@app.route('/test_recognition')
def test_recognition():
    stop_all_cameras()
    return render_template('recognize.html')

@app.route('/video_feed_recognize')
def video_feed_recognize():
    return Response(gen(recognize_face.recognizer_system),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)

