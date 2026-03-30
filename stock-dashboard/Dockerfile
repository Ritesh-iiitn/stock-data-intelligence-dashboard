FROM python:3.9-slim

WORKDIR /app

# Install dependencies based on current platform layer mapping
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy logic engines
COPY . .

# Server mapping configuration
EXPOSE 8000

# Standalone execution
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
