# backend/Dockerfile

# 1. Use Python 3.11
FROM python:3.11-bookworm

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set work directory
WORKDIR /app

# 4. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies in correct order
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

##Try to solve dependencies version problem
#COPY requirements_names.txt .
#RUN pip install --upgrade pip && \
#	pip install -r requirements_names.txt

# 6. Copy the application code
COPY . .

# 7. Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
