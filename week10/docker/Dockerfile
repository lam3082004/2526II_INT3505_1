FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs

EXPOSE 5012

ENV FLASK_DEBUG=0
ENV LOG_LEVEL=INFO
ENV ENVIRONMENT=production

CMD ["python", "src/server.py"]
