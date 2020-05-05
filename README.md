# microservice-reasoning-task

This microservice renders a view to let a user upload input for the EYE reasoner and execute the reasoner.

## Dependencies

You can use the DOCKERFILE to create a Docker image and run the service with Docker

### Without Docker

1. Linux
2. python3
3. packages: see requirements.txt
4. Local installation of the [EYE reasoner](http://sourceforge.net/projects/eulersharp/files/eulersharp/) (located in /opt/eye/eye.sh) and its dependencies
   - swipl
   - curl
   - carl
   - cturtle

## Install and run

1. [sudo] docker build -t reasoning-task .
2. [sudo] docker run -p 8080:8080 reasoning-task


### Without Docker

1. ``pip3 install -r requirements.txt``
2. start with ``python3 reasoning-task.py``
3. Go to http://localhost:8080/reasoning-task


## Publish on Dockerhub
See [microservice-template](https://github.com/nie-ine/microservice-template)
