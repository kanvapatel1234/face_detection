import cv2
import numpy as np
from PIL import Image

from facenet_pytorch import MTCNN, InceptionResnetV1

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from database.attendance_service import mark_attendance


# -------------------------
# Load Models
# -------------------------

mtcnn = MTCNN(
    image_size=160
)

resnet = InceptionResnetV1(
    pretrained="vggface2"
).eval()


# -------------------------
# Load Embeddings
# -------------------------

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

embeddings = np.load(
    os.path.join(
        BASE_DIR,
        "embeddings",
        "embeddings.npy"
    )
)

labels = np.load(
    os.path.join(
        BASE_DIR,
        "embeddings",
        "labels.npy"
    )
)

THRESHOLD = 0.7

print(
    f"\nLoaded {len(labels)} face embeddings"
)


# -------------------------
# Recognition Function
# -------------------------

def recognize_image(image):

    face = mtcnn(image)

    if face is None:

        return {
            "success": False,
            "message": "No face detected"
        }

    query_embedding = (
        resnet(
            face.unsqueeze(0)
        )
        .detach()
        .numpy()[0]
    )

    similarities = np.dot(
        embeddings,
        query_embedding
    ) / (
        np.linalg.norm(
            embeddings,
            axis=1
        )
        *
        np.linalg.norm(
            query_embedding
        )
    )

    best_index = np.argmax(
        similarities
    )

    best_similarity = float(
        similarities[best_index]
    )

    best_label = str(
        labels[best_index]
    )

    if best_similarity > THRESHOLD:

        attendance_result = mark_attendance(
            best_label
        )

        return {
            "success": True,
            "name": best_label,
            "similarity": round(
                best_similarity,
                4
            ),
            "attendance": attendance_result
        }

    return {
        "success": False,
        "message": "Unknown Person",
        "closest_match": best_label,
        "similarity": round(
            best_similarity,
            4
        )
    }


# -------------------------
# Webcam Capture
# -------------------------

def capture_from_camera():

    cap = cv2.VideoCapture(0)

    print("\nPress SPACE to capture")
    print("Press ESC to cancel")

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        cv2.imshow(
            "Face Recognition Camera",
            frame
        )

        key = cv2.waitKey(1)

        if key == 32:

            image = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            cap.release()
            cv2.destroyAllWindows()

            return Image.fromarray(
                image
            )

        elif key == 27:

            cap.release()
            cv2.destroyAllWindows()

            return None


# -------------------------
# Local Testing
# -------------------------

if __name__ == "__main__":

    image = capture_from_camera()

    if image is None:

        print("No image captured")
        exit()

    result = recognize_image(
        image
    )

    print("\n===== RESULT =====")

    for key, value in result.items():

        print(
            f"{key} : {value}"
        )