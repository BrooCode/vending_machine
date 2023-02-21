import boto3 
import cv2
import io
import calendar
import datetime
import uuid
import os
import json


def commodity_upload(img):
    img = cv2.imread(img)
    success, encoded_image = cv2.imencode('.png', img)
    processed = encoded_image.tobytes()
    # ACCESS_KEY = '*'
    # SECRET_KEY = '*'
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    bucket = s3.Bucket(name="resoluteai")

    date = datetime.datetime.utcnow()
    now = datetime.datetime.now()
    dt_string = now.strftime("%d%m%Y%H:%M:%S")
    utc_time = calendar.timegm(date.utctimetuple())
    filename = "development/" + str(utc_time) + str(dt_string) + ".png"
    bucket.upload_fileobj(io.BytesIO(processed), filename,ExtraArgs={'ACL': 'public-read',"ContentType":"image/png"})
    fileLink="https://resoluteai.s3.ap-south-1.amazonaws.com/"+filename
    return fileLink
