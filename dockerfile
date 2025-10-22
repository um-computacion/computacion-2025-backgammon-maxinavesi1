# Dockerfile - Para ejecutar tests del core
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del core y tests
COPY backgammon ./backgammon

# Comando por defecto: ejecutar tests del core
CMD ["python", "-m", "unittest", "discover", "-s", "backgammon/tests", "-p", "test_*.py"]