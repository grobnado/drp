
FROM python:3.12

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000
CMD ["python", "api/index.py"]
