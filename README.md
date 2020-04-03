# microservice-reasoning-task

This microservice renders a view to let a user upload input for the EYE reasoner and execute the reasoner.

## Dependencies
1. python3
2. packages: see requirements.txt
3. EYE reasoner and dependencies described in its installation guide
   - EYE: http://sourceforge.net/projects/eulersharp/files/eulersharp/
   - swipl
   - curl
   - carl
   - cturtle

## Install and run
1. ``pip install -r requirements.txt``
2. start with ``python3 json-task.py``

## Publish on Dockerhub
See [microservice-template](https://github.com/nie-ine/microservice-template)
