# microservice-reasoning-task

This microservice renders a view to let a user upload input for the EYE reasoner and execute the reasoner.

## Dependencies
1. Linux
2. python3
3. packages: see requirements.txt
4. EYE reasoner and dependencies described in its installation guide
   - EYE: http://sourceforge.net/projects/eulersharp/files/eulersharp/
   - swipl
   - curl
   - carl
   - cturtle

## Install and run
1. ``pip install -r requirements.txt``
2. For now, put a copy of your eye reasoner folder (should be in opt/ into the microservice-reasoning-task directory
   (i.e. eye/ with bin/eye.sh, lib/eye.pvm, src/eye.pl)
3. start with ``python3 json-task.py``
4. Go to http://localhost:8080/reasoning-task

## Publish on Dockerhub
See [microservice-template](https://github.com/nie-ine/microservice-template)
