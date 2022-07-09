FROM python:3.10.5

COPY requirements.txt ./requirements.txt
COPY producer.py ./producer.py

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","./producer.py"]