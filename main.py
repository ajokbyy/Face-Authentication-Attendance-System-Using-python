import register_face
import attendance
import recognize_face
import sys

def main():
    while True:
        print("\n=======================================")
        print(" FACE AUTHENTICATION ATTENDANCE SYSTEM ")
        print("=======================================")
        print("1. Register New Face")
        print("2. Mark Attendance")
        print("3. Test Face Recognition (No DB Write)")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            register_face.register()
        elif choice == '2':
            attendance.start_attendance()
        elif choice == '3':
            recognize_face.recognize()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
