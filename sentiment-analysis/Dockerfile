# base image
FROM ubuntu:18.04

# setting the directory in the container
COPY . /usr/src/app
WORKDIR /usr/src/app

# Installing update and upgrade along with python
RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Installing the other dependencies
RUN pip3 install -r requirements.txt

# Exposing the port
EXPOSE 5000

# The startup command
CMD [ "python3", "/usr/src/app/app.py" ]