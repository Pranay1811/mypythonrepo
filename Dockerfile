FROM python:3.12-slim

WORKDIR /app

# copy requirements then install (cacheable)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY app ./app

EXPOSE 8080

CMD ["python", "-u", "app/add.py"]
