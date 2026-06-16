FACE DETECTION ATTENDANCE SYSTEM

Overview

The Face Detection Attendance System is an application that automates attendance tracking using facial recognition technology. Users can enroll their faces into the system, and attendance is automatically marked when their face is recognized through a camera. The project combines FastAPI, OpenCV, MongoDB, and a simple web interface to provide an efficient attendance management solution.

Features

• Face Enrollment for new users
• Face Recognition using stored face embeddings
• Automatic Attendance Marking
• MongoDB Database Integration
• Web-based User Interface
• FastAPI Backend APIs
• Face Embedding Storage and Management

Project Structure

app.py
Main FastAPI application and API endpoints.
mongo.py
MongoDB connection and configuration.
database/attendance_service.py
Handles attendance-related database operations.
src/enrolling.py
Responsible for enrolling new users and generating face embeddings.
src/recognize.py
Performs face recognition using stored embeddings.
frontend/index.html
Main user interface.
frontend/script.js
Frontend logic and API communication.
frontend/style.css
Styling for the web interface.
embeddings/embeddings.npy
Stores generated face embeddings.
embeddings/labels.npy
Stores labels corresponding to embeddings.
dataset/
Stores face images used for enrollment and recognition.
requirements.txt
List of required Python packages.
.env
Environment variables and configuration settings.

Technologies Used

Backend:

Python
FastAPI
OpenCV
NumPy

Frontend:

HTML
CSS
JavaScript

Database:

MongoDB

Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

Windows:
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure the .env file with MongoDB connection details.

Running the Application

Start the FastAPI server:

uvicorn app:app --reload

The application will be available at:

http://127.0.0.1:8000

Workflow

Enroll a user by capturing face images.
Generate face embeddings from the captured images.
Store embeddings and user information.
Capture a face for recognition.
Compare the captured face with stored embeddings.
Mark attendance automatically when a match is found.
Save attendance records in MongoDB.

Future Enhancements

Real-time webcam streaming
Attendance reports and analytics
Admin dashboard
User authentication
Cloud deployment
Multi-camera support

Conclusion

This project demonstrates how facial recognition can be used to automate attendance management. By integrating FastAPI, OpenCV, MongoDB, and a web frontend, the system provides a simple and efficient solution for recording and managing attendance.