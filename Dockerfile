FROM python:3.11-slim-bullseye

WORKDIR /app

COPY main.py test_main.py ./

RUN pip install --no-cache-dir pytest==8.3.3

CMD ["pytest", "test_main.py", "-v", "--tb=short"]