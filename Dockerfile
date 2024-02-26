FROM python:3.11

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8099

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8099", "--reload"]