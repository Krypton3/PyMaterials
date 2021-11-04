# syntax=docker/dockerfile:1

# base image
FROM python:3.8-slim-buster

# working directory
WORKDIR /app

# copying the dependencies for this app
COPY requirements.txt requirements.txt

# Installing everything from requirements.txt file
RUN pip3 install -r requirements.txt

# Now we will copy everything else into the image
COPY . .

# defaul command when running the container
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
