FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backgammon ./backgammon
CMD ["python","-m","unittest","discover","backgammon/tests"]