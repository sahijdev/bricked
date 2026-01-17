from fastapi import FastAPI, UploadFile, File
import requests
import cv2
from PIL import Image
import io
import numpy as np

url = "https://api.brickognize.com/predict/"

app = FastAPI()

# Detect and extract all the different bricks in the image
@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    MIN_AREA = 500
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert()
    np_image = np.array(image)
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i, c in enumerate(contours):
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if area > MIN_AREA:
            part = np_image[y:y+h, x:x+w]
            cv2.imshow("Image", part)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return {"Return": "test"}