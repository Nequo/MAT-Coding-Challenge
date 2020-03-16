FROM python:3

COPY ./src /app
COPY track.csv /app/track.csv
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./backend.py"]
