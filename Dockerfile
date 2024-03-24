FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pay2u.wsgi"]
