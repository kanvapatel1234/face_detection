from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

# Test connection immediately
client.admin.command("ping")

db = client["face_attendance"]

attendance_collection = db["attendance"]

print("MongoDB Atlas Connected")