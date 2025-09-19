from fastapi import FastAPI, UploadFile, File
from classifier import Classifier
import shutil
import os

app = FastAPI()
c = Classifier()

INPUT_DIR = "./.temp_uploads"
os.makedirs(INPUT_DIR, exist_ok=True)


@app.get("/", tags=["Get Methods"])
async def home():
    return "Network File Classifier is up and running."


@app.post("/classify-pdf/")
async def classify_pdf(file: UploadFile = File(...)):
    file_location = os.path.join(INPUT_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = c.process_single_pdf(file_location)
    os.remove(file_location)

    return result
