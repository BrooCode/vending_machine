FROM python:3.9

COPY requirements.txt ./

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -

RUN apt install libgl1-mesa-glx -y

RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y


RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app2

ADD . /app2

EXPOSE 5050

CMD ["uvicorn", "api:app","--host","0.0.0.0","--port", "5050"]
