import pymongo
from datetime import datetime

# --- CONFIGURATION ---
DB_NAME = "face_attendance_db"
MONGO_URL = "mongodb://localhost:27017/"

# --- DATABASE CONNECTION ---
try:
    client = pymongo.MongoClient(MONGO_URL)
    db = client[DB_NAME]
    users_col = db["users"]
    attendance_col = db["attendance"]
    print(f"[INFO] Connected to MongoDB: {DB_NAME}")
except Exception as e:
    print(f"[ERROR] Could not connect to MongoDB. Ensure it is running. Error: {e}")
    exit()

def add_user(user_id, name, face_encoding):
    """
    Saves a new user to the database.
    face_encoding: List of numbers representing the face.
    """
    # Check if ID already exists
    if users_col.find_one({"user_id": user_id}):
        print(f"[WARNING] User ID {user_id} already exists!")
        return False
    
    user_data = {
        "user_id": user_id,
        "name": name,
        "face_encoding": face_encoding  # Store as list
    }
    users_col.insert_one(user_data)
    print(f"[SUCCESS] User {name} (ID: {user_id}) registered.")
    return True

def get_all_users():
    """
    Retrieves all users and their face encodings.
    Returns a list of dictionaries.
    """
    return list(users_col.find({}, {"_id": 0, "user_id": 1, "name": 1, "face_encoding": 1}))

def mark_attendance(user_id, action='in'):
    """
    Marks attendance for a user.
    action: 'in' or 'out'
    """
    user = users_col.find_one({"user_id": user_id})
    if not user:
        print(f"[ERROR] User ID {user_id} not found.")
        return None

    today_str = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    # Check for existing attendance record for today
    today_record = attendance_col.find_one({"user_id": user_id, "date": today_str})

    if action == 'in':
        if today_record:
            # Already punched in today
            return f"{user['name']} - Already Punched In"
        else:
            # Create new record
            attendance_data = {
                "user_id": user_id,
                "name": user["name"],
                "date": today_str,
                "punch_in_time": now_time,
                "punch_out_time": None
            }
            attendance_col.insert_one(attendance_data)
            print(f"[ATTENDANCE] {user['name']} - PUNCH IN at {now_time}")
            return f"Welcome {user['name']}! (Punch In)"
            
    elif action == 'out':
        if not today_record:
            # No record found to punch out from
            return f"{user['name']} - No Punch In Record"
        
        if today_record["punch_out_time"]:
            # Already punched out
            return f"{user['name']} - Already Punched Out"
            
        # Update record
        attendance_col.update_one(
            {"_id": today_record["_id"]},
            {"$set": {"punch_out_time": now_time}}
        )
        print(f"[ATTENDANCE] {user['name']} - PUNCH OUT at {now_time}")
        return f"Goodbye {user['name']}! (Punch Out)"
    
    return None

def get_attendance_logs():
    """
    Fetches all attendance records, sorted by date and time descending.
    """
    return list(attendance_col.find({}, {"_id": 0}).sort([("date", -1), ("punch_in_time", -1)]))
