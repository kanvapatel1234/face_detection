from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["face_attendance"]

attendance_collection = db["attendance"]

print("MongoDB Connected")