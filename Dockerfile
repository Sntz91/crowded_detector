FROM python:3.10

ADD crowded_detector.py .
COPY requirements.txt .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install -r requirements.txt

CMD ["python", "/crowded_detector.py"]
