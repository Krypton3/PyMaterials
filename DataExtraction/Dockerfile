# base image
FROM python:3.12-slim

# Set environment variables to avoid Python buffering and set Flask to development mode (optional)
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development

# working directory
WORKDIR /app

# copying the dependencies for this app
COPY requirements.txt .

# Installing everything from requirements.txt file
RUN pip3 install --no-cache-dir -r requirements.txt

# Now we will copy everything else into the image
COPY . .

# defaul command when running the container
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
