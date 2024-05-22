from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import cv2
import pytesseract
import os
from tempfile import NamedTemporaryFile

app = FastAPI()

# Path to Tesseract executable (you need to install Tesseract OCR)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Function to process each frame of the uploaded video and detect text
def detect_text_from_video(video_path: str, frame_skip: int = 30) -> List[str]:
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # List to store detected text from each frame
    detected_text = []

    frame_count = 0

    while True:
        # Read frame from the video
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1

        # Process every Nth frame to speed up processing
        if frame_count % frame_skip != 0:
            continue

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize frame to reduce processing time
        gray = cv2.resize(gray, (gray.shape[1] // 2, gray.shape[0] // 2))

        # Apply thresholding or other preprocessing techniques if needed

        # Use pytesseract to detect text
        text = pytesseract.image_to_string(gray)

        # Add detected text to the list
        detected_text.append(text)

    # Release the video capture object
    video_capture.release()

    return detected_text

@app.post("/detect_text_from_video/")
async def detect_text_from_uploaded_video(video_file: UploadFile = File(...)):
    # Save the uploaded video to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.file.read())
        temp_video_path = temp_video.name

    try:
        # Detect text from the uploaded video
        detected_text = detect_text_from_video(temp_video_path)

    finally:
        # Delete the temporary video file
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

    return {"detected_text": detected_text}

@app.get("/")
def home():
    return {"message": "Welcome to the Video Text Detection API!"}
