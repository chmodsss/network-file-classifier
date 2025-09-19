from fastapi import FastAPI, UploadFile, File
from classifier import Classifier
import shutil
import os
from config import TEMP_DIR

app = FastAPI()
c = Classifier(mock_flag=False, model="gpt-4o")


os.makedirs(TEMP_DIR, exist_ok=True)


@app.get("/", tags=["Get Methods"])
async def home():
    return "Network File Classifier is up and running."


@app.post("/classify-pdf/")
async def classify_pdf(file: UploadFile = File(...)):
    file_location = os.path.join(TEMP_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = c.process_single_pdf(file_location)
    os.remove(file_location)

    return result
