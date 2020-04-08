# microservice-reasoning-task

This microservice renders a view to let a user upload input for the EYE reasoner and execute the reasoner.

## Dependencies
1. Linux
2. python3
3. packages: see requirements.txt
4. Local installation of the [EYE reasoner](http://sourceforge.net/projects/eulersharp/files/eulersharp/) and its dependencies
   - EYE (located in /opt/eye/eye.sh) 
   - swipl
   - curl
   - carl
   - cturtle

## Install and run
1. ``pip install -r requirements.txt``
3. start with ``python3 json-task.py``
4. Go to http://localhost:8080/reasoning-task

## Publish on Dockerhub
See [microservice-template](https://github.com/nie-ine/microservice-template)
