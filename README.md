### Hexlet tests and linter status:
[![Actions Status](https://github.com/AlexVSSP/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/AlexVSSP/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/121dcb63c548b325f700/maintainability)](https://codeclimate.com/github/AlexVSSP/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/121dcb63c548b325f700/test_coverage)](https://codeclimate.com/github/AlexVSSP/python-project-52/test_coverage)
[![Python CI](https://github.com/AlexVSSP/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/AlexVSSP/python-project-52/actions/workflows/pyci.yml)

Railway: 
https://task-manager-alexvssp.up.railway.app

### Requirements
- Python version: ^3.8
- Poetry version: ^1.0.0

### Description of the project:
This project supports the Task Manager web application, in which you can create and edit
users, tasks, task statuses, as well as labels that are an alternative to categories.

The demo project is presented at the following **[link](https://task-manager-alexvssp.up.railway.app)**. 
You can register in it as a new user and experiment with all the elements of the project.

## How to install

- First you need to clone the repository:
```
    git clone git@github.com:AlexVSSP/python-project-52.git
    cd python-project-52
```
- Use command to install all dependencies with Poetry:
```
    make install
```

- Create a file .env in the root of the project with the command:
```
    touch .env
```

- In the file, create the following variables:
1. SECRET_KEY='Django secret key'
2. DEBUG='True or False'
3. DATABASE_URL='Your database url'
4. ROLLBAR_KEY='roll bar key'

- To prepare the database, use the following commands:
```
    make migrations
    make migrate
```

## How to use

- To start the server on the local host, use the following command (and after that click on the appeared link):
```
    make start
```