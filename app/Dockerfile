# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /app
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "run.py"]
