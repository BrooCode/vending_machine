from fastapi import FastAPI, Request, Form
from fastapi import FastAPI
import shutil
from starlette.middleware.cors import CORSMiddleware
import detect as detect
import cv2,os,shutil
import random
import s3upload as upload
import base64
import numpy as np
from fastapi import File, UploadFile
from PIL import Image
from io import BytesIO
import result as result
from imageio import imread
import io
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

def read_imagefile(file) -> Image.Image:
    return np.array(Image.open(BytesIO(file)))

def read_root(image: Image.Image):
    uid = random.randint(0,10000)
    temp_file_name = str(uid) + "commodity.jpg"
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(temp_file_name,image_rgb)
    result_filename,count = detect.run(temp_file_name,"best_ckpt.pt")
    try:
        filelink = upload.commodity_upload(result_filename)
    except:
        print("Unable to upload")
    os.remove(result_filename)
    return filelink,count

@app.get("/vending_machine")
async def form_post(request: Request):
        req_info = await request.json()
        print(req_info)
        b64_string = req_info["img"]
        uid = random.randint(0,10000)
        temp_file_name = str(uid) + "commodity.jpg"
        img = imread(io.BytesIO(base64.b64decode(b64_string)))
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(temp_file_name,image_rgb)
        result_filename,count = detect.run(temp_file_name,"best_ckpt.pt")
        os.remove(temp_file_name)
        print(result_filename)
        try:
            filelink = upload.commodity_upload(result_filename)
        except:
            print("Unable to upload")
        os.remove(result_filename)
        return result.response(filelink,count) 


@app.get("/vending_machine_ui")
async def form_post(request: Request):
    result = "Upload an image"
    return templates.TemplateResponse('vending_machine_ui.html', context={'request': request, 'result': result}) 


@app.post("/vending_machine_ui")
async def form_post(request: Request,image: UploadFile = File(...)):
    image = read_imagefile(await image.read())
    filelink,count =  read_root(image)
    return templates.TemplateResponse('vending_machine_ui.html', context={'request': request, 'result': filelink ,'commodity': count})
