import shutil

import form as form
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import cv2
import pyzbar.pyzbar as pyzbar

import os
import requests
from PIL import Image 

def detect():
    camera = cv2.VideoCapture(0)
    data = ''
    while True:
        ret, frame = camera.read() 
        barcodes = pyzbar.decode(frame) 
        data = ''
        for barcode in barcodes:
            data = barcode.data.decode('utf-8')
        if data != '':
            with open('data.txt', 'w') as file:
                file.write(data)
            break
        if cv2.waitKey(1) == ord('q'):
            break
        cv2.imshow('', frame)
    camera.release()
    cv2.destroyAllWindows()
    return data

# def scan_image():
#     image = "C:\Users\Caesar\Downloads\\barcode1.jpg"
#     barcodes = pyzbar.decode(Image.open(image))
#     data = ''
#     for barcode in barcodes:
#         data = barcode.data.decode('utf-8')
#     if data != '':
#         with open('data.txt', 'w') as file:
#             file.write(data)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/scanning")
async def scan():
    data=detect()
    return {"barcode":data}
    
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):

    for file in files:
        with open(f'{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"filenames": [file.filename for file in files]}


# image save
