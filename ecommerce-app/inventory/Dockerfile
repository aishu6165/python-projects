FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && \
    echo "Installed packages:" && pip freeze
EXPOSE 5006
CMD ["python", "app.py"]
