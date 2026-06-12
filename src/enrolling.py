import os
import numpy as np
from PIL import Image

from facenet_pytorch import MTCNN, InceptionResnetV1

mtcnn = MTCNN(image_size=160)

resnet = InceptionResnetV1(
    pretrained='vggface2'
).eval()
DATASET_DIR = "dataset"

embeddings = []
labels = []

for person_name in os.listdir(DATASET_DIR):

    person_path = os.path.join(
        DATASET_DIR,
        person_name
    )

    if not os.path.isdir(person_path):
        continue

    print(f"Processing {person_name}")

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        try:
            image = Image.open(image_path).convert("RGB")

        except Exception:
            continue
        face = mtcnn(image)

        if face is None:
            print(
                f"No face found: {image_name}"
            )
            continue
        embedding = (
            resnet(
                face.unsqueeze(0)
            )
            .detach()
            .numpy()
        )

        print(f"Processed: {person_name}/{image_name}")

        embeddings.append(
            embedding[0]
        )

        labels.append(
            person_name
        )


os.makedirs(
    "embeddings",
    exist_ok=True
)

np.save(
    "embeddings/embeddings.npy",
    np.array(embeddings)
)

np.save(
    "embeddings/labels.npy",
    np.array(labels)
)

print("Enrollment completed!")