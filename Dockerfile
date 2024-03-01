FROM python:3.10-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN apt-get update && apt-get install -y git gcc python3-dev ffmpeg libsm6 libxext6
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
