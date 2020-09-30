# microservice-reasoning-task

This microservice is part of the microservice pipline in [inseri](https://github.com/nie-ine/inseri). The service provides the possibility to conduct machine reasoning using the [EYE reasoner](http://sourceforge.net/projects/eulersharp/files/eulersharp/).

The microservice accepts both a FileList object sent through an HTML form or JSON data of the file's names and contents.

There's an inseri app to select files locally and send them to the microservice but the service also provides its own HTML interface to select files for a reasoning session.

## Run and Develop Locally

### Dependencies

1. Ubuntu 18.04
2. Python 3
3. packages: see requirements.txt
4. Local installation of the EYE reasoner (located in /opt/eye/bin/eye.sh) and its dependencies
   - swipl
   - curl
   - carl
   - cturtle

### Install and Run

1. Clone the repository
1. cd into the repository
1. Run ``pip3 install -r requirements.txt`` to fetch the needed Python packages (you might want to do this within a virtual Python environment)
2. Run ``python3 reasoning-task.py`` to start the service
1. POST FileList object or JSON to http://localhost:50001 (see below)
3. Or use the GUI to create the POST by opening:  
   - http://localhost:50001 for sending a FileList object
   - http://localhost:50001?gui=json for sending JSON data

## Run with Docker

1. Build the image: ``[sudo] docker build -t nieine/microservice-reasoning-task .``
1. Run the container: ``[sudo] docker run -p 50001:50001 nieine/microservice-reasoning-task``
1. POST FileList object or JSON to http://localhost:50001 (see below)
3. Or use the GUI to create the POST by opening:  
   - http://localhost:50001 for sending a FileList object
   - http://localhost:50001?gui=json for sending JSON data

## Call the Service in a RESTful Way

If the service is running, you can POST either a FileList object or JSON. Either way, you will receive a turtle file as a response. 

### FileList

Currently, please use the GUI interface and the developer tools to get an idea on how the FileList looks like. 


### JSON

Body, e.g.:

```
{
    "data": {
        "files": [
            {
                "file": "cindy.ttl",
                "content": "@prefix ppl: <http://example.org/people#>. @prefix foaf: <http://xmlns.com/foaf/0.1/>. ppl:Cindy foaf:knows ppl:John."
            }
        ],
        "urls": [
        ]
    },
    "rules": {
        "files": [
            {
                "file": "cindyRule.n3",
                "content": "@prefix ppl: <http://example.org/people#>. @prefix foaf: <http://xmlns.com/foaf/0.1/>. { ppl:Cindy foaf:knows ppl:John. } => { ppl:John foaf:knows ppl:Cindy. } ."
            }
        ],
        "urls": [
        ]
    },
    "queries": {
        "files": [
            {
                "file": "cindyQuery.n3",
                "content": "{ ?a ?b ?c. } => { ?a ?b ?c. }."
            }
        ],
        "urls": [
        ]
    }
}
```

## Publish on Dockerhub

1. Build the image: ``[sudo] docker build -t nieine/microservice-reasoning-task:YYYY-MM-DD .``
1. Push the image: ``[sudo] docker push nieine/microservice-reasoning-task:YYYY-MM-DD``