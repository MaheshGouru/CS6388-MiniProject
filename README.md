# CS6388-MiniProject
This repository is intended to server as a bootstrap for a fully docker based Design Studio development with WebGME to support modeling of Data Engineering on cloud providers such as Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure (AZURE).
The Design Studio allows model editing, simulation, and some limited model-checking functionality. As such the studio implements the finite state machine domain. For its special simulator visualization, it uses the [JointJS](https://www.jointjs.com/) javascript library.

## Description of Domain

## Type Use-Cases of the Domain

## How to start modeling Data Engineering Pipelines

## Features & FAQs

## Installation of the Design Studio

### Initialization
The easiest way to start using this project is to fork it in git. Alternatively, you can create your empty repository, copy the content and just rename all instances of 'WDeStuP' to your liking. Assuming you fork, you can start-up following this few simple steps:
- install [Docker-Desktop](https://www.docker.com/products/docker-desktop)
- clone the repository
- edit the '.env' file so that the BASE_DIR variable points to the main repository directory
- `docker-compose up -d`
- connect to your server at http://localhost:8888

## Main docker commands
All of the following commands should be used from your main project directory (where this file also should be):
- To **rebuild** the complete solution `docker-compose build` (and follow with the `docker-compose up -d` to restart the server)
- To **debug** using the logs of the WebGME service `docker-compose logs webgme`
- To **stop** the server just use `docker-compose stop`
- To **enter** the WebGME container and use WebGME commands `docker-compose exec webgme bash` (you can exit by simply closing the command line with linux command 'exit') 
- To **clean** the host machine of unused (old version) images `docker system prune -f`

## Using WebGME commands to add components to your project
In general, you can use any WebGME commands after you successfully entered the WebGME container. It is important to note that only the src directory is shared between the container and the host machine, so you need to additionally synchronize some files after finishing your changes inside the container! The following is few scenarios that frequently occur:

### Adding new npm dependency
When you need to install a new library you should follow these steps:
- enter the container
- `npm i -s yourNewPackageName`
- exit the container
- copy the package.json file `docker compose cp webgme:/usr/app/package.json package.json`

### Adding new interpreter/plugin to your DS
Follow these steps to add a new plugin:
- enter the container `docker compose exec webgme bash`
- for JS plugin: `webgme new plugin MyPluginName`
- for Python plugin: `webgme new plugin MyPluginName --language Python`
- exit container `exit`
- copy webgme-setup.json `docker compose cp webgme:/usr/app/webgme-setup.json webgme-setup.json`
- copy webgme-config `docker compose cp webgme:/usr/app/config/config.webgme.js config/config.webgme.js`

### Adding new visualizer to your DS
Follow these steps to add a new visualizer:
- enter the container `docker compose exec webgme bash`
- `npm run webgme new viz MyVisualizerName`
- exit container `exit`
- copy webgme-setup.json `docker compose cp webgme:/usr/app/webgme-setup.json webgme-setup.json`
- copy webgme-config `docker compose cp webgme:/usr/app/config/config.webgme.js config/config.webgme.js`

### Adding new seed to your DS
Follow these steps to add a new seed based on an existing project in your server:
- enter the container `docker compose exec webgme bash`
- `webgme new seed MyProjectName -- --seed-name MySeedName`
- exit container with `exit`
- copy webgme-setup.json `docker compose cp webgme:/usr/app/webgme-setup.json webgme-setup.json`
- copy webgme-config `docker compose cp webgme:/usr/app/config/config.webgme.js config/config.webgme.js`