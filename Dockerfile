FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/M-Irshad-cloud/devops-beginner-track"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
