FROM python:3.7-slim

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY configs /app/configs

RUN pip install -r /app/configs/requirements.txt

COPY GetRekognition.py /app/GetRekognition.py

WORKDIR /app

# YOU MUST ENTER INSTAGRAM URL AS ARGUMENT...

CMD ["python3", "GetRekognition.py", "romanreigns"]
