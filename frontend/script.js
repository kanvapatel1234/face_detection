const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

const openBtn =
    document.getElementById("openBtn");

const captureBtn =
    document.getElementById("captureBtn");

const closeBtn =
    document.getElementById("closeBtn");

const resultDiv =
    document.getElementById("result");


let stream = null;


// ------------------------
// Open Camera
// ------------------------

openBtn.addEventListener(
    "click",
    async () => {

        try {

            stream =
                await navigator.mediaDevices
                    .getUserMedia({
                        video: true
                    });

            video.srcObject = stream;

            resultDiv.innerHTML =
                "Camera Opened";

        } catch (error) {

            console.error(error);

            resultDiv.innerHTML =
                "Unable to access webcam";
        }

    }
);


// ------------------------
// Close Camera
// ------------------------

closeBtn.addEventListener(
    "click",
    () => {

        if (stream) {

            stream
                .getTracks()
                .forEach(
                    track => track.stop()
                );

            video.srcObject = null;

            resultDiv.innerHTML =
                "Camera Closed";
        }

    }
);


// ------------------------
// Capture Attendance
// ------------------------

captureBtn.addEventListener(
    "click",
    async () => {

        if (!stream) {

            resultDiv.innerHTML =
                "Open camera first";

            return;
        }

        resultDiv.innerHTML =
            "Processing...";

        canvas.width =
            video.videoWidth;

        canvas.height =
            video.videoHeight;

        const ctx =
            canvas.getContext("2d");

        ctx.drawImage(
            video,
            0,
            0,
            canvas.width,
            canvas.height
        );

        canvas.toBlob(

            async (blob) => {

                const formData =
                    new FormData();

                formData.append(
                    "file",
                    blob,
                    "capture.jpg"
                );

                try {

                    const response =
                        await fetch(
                            "http://127.0.0.1:8000/recognize",
                            {
                                method: "POST",
                                body: formData
                            }
                        );

                    const data =
                        await response.json();

                    console.log(data);

                    if (
                        data.success
                    ) {

                        resultDiv.innerHTML =
                            `
                            <h3>Attendance Marked</h3>

                            <p>
                                Name:
                                ${data.name}
                            </p>

                            <p>
                                Similarity:
                                ${data.similarity}
                            </p>

                            <p>
                                Status:
                                ${data.attendance}
                            </p>
                            `;

                        // Auto Close Camera

                        stream
                            .getTracks()
                            .forEach(
                                track => track.stop()
                            );

                        video.srcObject =
                            null;

                        stream = null;

                    } else {

                        resultDiv.innerHTML =
                            `
                            <h3>
                                Recognition Failed
                            </h3>

                            <p>
                                ${data.message}
                            </p>

                            <p>
                                Similarity:
                                ${data.similarity}
                            </p>
                            `;
                    }

                } catch (error) {

                    console.error(
                        error
                    );

                    resultDiv.innerHTML =
                        "Server Error";
                }

            },

            "image/jpeg"

        );

    }
);