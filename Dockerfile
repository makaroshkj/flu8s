FROM python:alpine3.18
WORKDIR /app 
COPY app .
RUN pip3  install --upgrade pip -r requirements.txt
ENTRYPOINT python app.py