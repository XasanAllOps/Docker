[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=black)](#)

## Containerizing a Simple Django App with Docker 

## Check Python Version

  - `python3 --version` = Output: Python:3.13.3
  - Python is the langauge Django is built-on and as a result it is important to have python installed or else Django will not work.

## Generating `requirements.txt`
  - `pip freeze > requirements.txt`
  - `freeze`: captures the version of the installation at the time to allow consistent builds

## Understanding `ALLOWED_HOSTS` in Django:
  - In settings.py, django uses `ALLOWED_HOSTS` to prevent HTTP Host header attacks
  - I originally encountered errors like: `Invalid HTTP_HOST header: <my-public-ip>:8000/demo`
  - To remediate this problem I added my EC2 Public IP or domain to `ALLOWED_HOSTS`

## Dockerfile (Breakdown)

  - `FROM python:3.13-slim`: Uses a lightweight version of Python 3.13 as the base image
  
  - `WORKDIR /app`: Sets the working directory inside the container & prevents hardcoding full paths

  - `COPY requirements.txt /app`: Copy `requirements.txt` file from local computer into container's /app folder. This file lists all Python packages Django needs.

  - `COPY devops /app/`: copy entire devops folder (django project) into /app in the container.

  - `RUN pip install --no-cache-dir -r requirements.txt`: Installs the required Python dependencies inside the container. `--no-cache-dir` keeps the image small by skipping cache storage.

  - `COPY devops/ .`: Copies the Django project files (e.g., `manage.py`, `settings.py`, `demo/` & more) into the container's `/app`. This step brings in all the code needed to run the Django website.

  - `EXPOSE 8000`: Instructs Docker that this container listens on port 8000 | -p 8000:8000

  - `CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]`: Runs Django's development server

  - `SHELL ["/bin/bash", "-c"]`: tell Docker to use bash shell for the next commands

## Setting Up Docker on AWS EC2

  - Spin up an Ubuntu EC2 Instance
  - SSH into your EC2 (`ssh -i "<KEY>" ubuntu@<ec2-public-key>`)
  - Run `sudo apt update && sudo apt install -y docker.io`
  - Run `sudo systemctl status docker` to check Docker status 🟢
  - Run `sudo usermod -aG docker ubuntu` to add ubuntu user to Docker group
  - Log out and then log back in 
  - Clone the repository containing the project: `git clone https://github.com/<username>/<repo>.git`
  - Run `docker build -t <>:latest`
  - Run `docker run -it -p 8000:8000 <>:latest`
  - Check if application is accessible from the internet: `curl http://<ec2-public-ip>:8000` 🧐
  - Access the app in browser: `http://<ec2-public-ip>:8000/demo`

## 🚨 Make Port 8000 Accessible on EC2

  - To access your Django app from your browser via `http://<your-ec2-public-ip>:8000/demo`, you must allow external traffic on port 8000 in your EC2 instance's security group.

## A Diagram with Visual Breakdown of My DockerFile:

```sql
┌────────────────────────────────────┐
│         Your Host Machine          │
│                                    │
│    Docker build . -t test-app      │
│ ┌───────────────────────────────┐  │
│ │  Dockerfile Instructions      │  │
│ │-----------------------------  │  │
│ │ FROM python:3.13-slim         │  │ ← Base OS
│ │ WORKDIR /app                  │  │ ← Folder for app
│ │ COPY requirements.txt .       │  │ ← Bring in deps list
│ │ RUN pip install ...           │  │ ← Install deps
│ │ COPY devops/ .                │  │ ← Copy Django app
│ │ EXPOSE 8000                   │  │ ← Tell Docker port to use
│ │ CMD ["python", "manage.py"...]│  │ ← Start Django
│ └───────────────────────────────┘  │
└────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│     Running Container on EC2/AWS       │
│                                        │
│ docker run -it -p 8000:8000 test-app   │
│                                        │
│  - Host port 8000 → container:8000     │
│  - Accessible from browser via:        │
│    http://<ec2-public-ip>:8000         │
└────────────────────────────────────────┘
```
