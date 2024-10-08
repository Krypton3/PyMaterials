## PyMaterials is a public repo to present different learning materials using python

### Module #1: Data Extraction

This module is based on Docker, Python, Flask, BeautifulSoup and Requests. The primary learning curve is to present docker. This module will present the following two questions:

- How to use docker in development level?
- How to use docker image, container, compose?

#### How to deploy the app locally?

- Clone the repository
- Execute: `cd DataExtraction/`
- Build and Run the container Image: `docker-compose -f docker-compose.dev.yml up --build`

#### Docker Compose Consists of the Following Commands:
- `docker build --tag <tag_name> .` | "." mean it will look for the Dockerfile to build the image.
- `docker run -p 5000:5000 <tag_name>` | "-p 5000:5000" means container listens to port 5000. Therefore, mapping the docker port to host port is important. Otherwise you will not be able to see the app in action. 
- Alt.: `docker run -d 5000:5000 <tag_name>` | "-d" means running the container in the detached mode. 
- Alt.: `docker run -d -p 5000:5000 --name <custom_name> <tag_name>` | You can give a custom name to your container.
- To see the images: `docker images`
- To see the running containers: `docker ps -a`
- To see all the containers: `docker ps`

We generally use docker compose to avoid all these commands. 

#### How to see the container details?
- `docker exec -it <container_name> /bin/bash`
- `ls` : You will be able to see the "marvel.csv" dataset which is created while deploying this app.

This module usage db "mysql", just for demo purpose. This app has two APIs to invoke the DB and Retrieve from it.
- How to use the database in docker? : https://docs.docker.com/language/python/develop/
- Invoking the DB: curl http://localhost:5000/initdb (After deploying the application - terminal)
- Retrieving from the DB: curl http://localhost:5000/widgets (After deploying the application - terminal)

#### What about the data extraction part?
This app will create a dataset using the "MarvelExtraction.py" file. All the general information of the marvel movies will be stored inside a CSV file! 

## Module #2: Docker + Flask + Celery + Redis

- An example of how to use multi-container docker!
- How to use celery and redis in an app?
- Command to Start: `docker-compose -f docker-compose.development.yml up --build`
- To find the dataset:
    - `docker exec -it <worker-container-id> /bin/sh`
    - You will find `marvel.csv`

## Module #3: Sentiment Analysis (It will be updated!)

The main purpose of this module is to make a docker image using Dockerfile. 

- How did I create an image?    
    - First, we need a base image: `FROM ubuntu:18.04`
    - Then, since this app is based on python, then we need to install python3 and It is standard to install all the followings: `RUN apt-get update | RUN apt-get upgrade -y | RUN apt-get install -y python3 | RUN apt-get install -y python3-pip`
    - Now we have everything we need to run a python script using this image. 
    - In addition to the app, we need to install every dependencies for the app using `RUN pip3 install -r requirements.txt` and exposed the port to `5000`.
    - Lastly, we set the startup command to run the app, which is `CMD [ "python3", "/usr/src/app/app.py" ]`
- Using docker compose? => `docker-compose -f docker-compose.yml up --build`