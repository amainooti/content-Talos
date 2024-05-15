from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import cv2
import pytesseract

app = FastAPI()

# Path to Tesseract executable (you need to install Tesseract OCR)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Function to process each frame of the uploaded video and detect text
def detect_text_from_video(video_path: str) -> List[str]:
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # List to store detected text from each frame
    detected_text = []

    while True:
        # Read frame from the video
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
    with open("temp_video.mp4", "wb") as video:
        video.write(video_file.file.read())

    # Detect text from the uploaded video
    detected_text = detect_text_from_video("temp_video.mp4")

    # Delete the temporary video file
    # You may want to handle temporary file cleanup differently based on your application requirements
    import os
    os.remove("temp_video.mp4")

    return {"detected_text": detected_text}

@app.get("/")
def home():
    return {"message": "Welcome to the Video Text Detection API!"}
