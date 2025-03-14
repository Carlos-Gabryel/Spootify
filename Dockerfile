#
FROM python:3.13:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --nocache-dir -r requirements.txt

COPY . . 

CMD ["python", "src/auto/spotify.py"]
