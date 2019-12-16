# Django 2.0+ project template

This is a simple Django 2.0+ project. Here I build a Stack Overflow clone called Answerly. Users can register for Answerly and will be able to ask and answer questions. A question's asker will also be able to accept answers to mark them useful and search similar type of questions.

## Features

- Django 2.0+
- Uses [Pipenv](https://github.com/kennethreitz/pipenv) - the officially recommended Python packaging tool from Python.org.
- Development, Staging and Production settings with [django-configurations](https://django-configurations.readthedocs.org).
- PostgreSQL database support with psycopg2.
- Using [Elasticsearch](https://www.elastic.co/) for finding answers. 
- For testing, Django integration tests, Selenium integration tests and [Coverage](https://coverage.readthedocs.io/en/coverage-5.0/) has been used.
- Deploying project using Apache, mod_wsgi in Docker.

## How to install

```bash
$ git clone https://github.com/shourya1997/django-stackoverflow-clone

# -- developement requirements file
$ pip install -r requirements.developement.txt

# -- production requirements file
$ pip install -r requirements.production.txt

```

## How to run

```bash

# -- common settings
$ python manage.py --settings=config.common_settings

```
### For running in production settings

Set the Environment variables in *Apache Server/localhost* (where ever you are deploying) mentioned in [answerly.ini](answerly.ini) and then run the following.

```bash

$ python manage.py --settings=config.production_settings

```

## Deployment

It is possible to deploy to Heroku/EC2 or to your own server. We will set all the services through docker containers and bind the ports to localhost of every service.

### Docker 

```bash
# Run Apache and bind to localhost port 80
$ sudo docker run -d -p 80:80 httpd 

# Pull Elasticsearch and bind to localhost: 9200 and 9300
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:7.4.2
$ docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.4.2 

# Pull postrgeSQL and bind to localhost: 5432
## stop local postgres if port already in use or stop conatiner which is might be using the port
$ sudo docker run -d -p 5432:5432 postgres:12.1

# Getting inside container
$ sudo docker exec -it <container id> bash

# Install packages in Apache Docker
$ apt install -y $(cat answerly/ubuntu/packages.txt)

# Set Postgres permissions in Postgres contaniner
$ bash postgres/make_database.sh

# IP address of docker container 
$ sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container ID>

# Commit container with required libraries
$ sudo docker commit <container NAMES> <NEW Container NAME>:<TAG>

# Collect static
$ python3 manage.py collectstatic --settings=config.production_settings --no-input   
```

TODO: Make DOCKERFILE for the above process.

## License

The MIT License (MIT)

Copyright (c) 2012-2017 José Padilla

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.