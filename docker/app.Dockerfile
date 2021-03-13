FROM python:3.9

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Make command output appear progressively as the application runs.
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["./main.py"]
