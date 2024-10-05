# Use a specific Python version for stability
FROM python:3.12.1-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to avoid Python buffering and set Flask to development mode
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development

# Set the working directory
WORKDIR /app

# Copy the requirements.txt into the image
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the image
COPY . .

# Expose port 8000 to allow communication to/from the container
EXPOSE 8000

# Default command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
