FROM python:3.11-slim

# set workdir
WORKDIR /app

# install system deps for pip if needed (none required for PyMySQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]