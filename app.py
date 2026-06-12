from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

from src.recognize import recognize_image
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Face Attendance API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "Face Attendance API Running"
    }


@app.post("/recognize")
async def recognize(
    file: UploadFile = File(...)
):

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    result = recognize_image(
        image
    )
    return result

    