FROM python:3.9.6

WORKDIR app/

COPY . .
COPY ./ssl /ssl

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
