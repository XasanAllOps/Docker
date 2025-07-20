## Docker notes

Simple project on how to containerise an a Django App

How to check what version of an application you are on?
  - In this case I will run python3 --version = Python 3.13.3
  - Python is the langauge Django is built-on and as a result it is important to have python installed or else Django will not work
  - To check if Django is installed run `python3 -m django --version`.
  - In this instance it will out either of two: The version or "No module named django"
  - 

Dockerfile
  - FROM ubuntu : selecting ubuntu as the base operating system the container will run in
  - WORKDIR /app : to set the working directory inside the container to /app
  - `COPY requirements.txt /app/`: copy `requirements.txt` file from local computer into container's /app folder
  - `COPY devops /app/`: copy entire devops folder (django project) into /app in the container
  - `RUN apt-get update && apt-get install -y python3 python3-pip python3-venv`: install the necessary packages
  - `SHELL ["/bin/bash", "-c"]`: tell Docker to use bash shell for the next commands
  - RUN python3 -m venv venv1 && \
    source venv1/bin/activate && \
    pip install --no-cache-dir -r requirements.txt : 
      - tells pip to install all the packages your app needs (requirements, can name it whatever you like)
      - `freeze`: captures the version of the installation at the time
      - `--no-cache-dir`: prevents pip from saving temp files, save space in the docker image, makes the image smaller and cleaner
      - `-r`: tells pip to 'read'/`-r` a list of packages in the file.
  - `EXPOSE 8000`: Docker container to listen on port 8000

Install Docker in a virtual container

- Run `sudo apt-get update && sudo apt-get install -y docker.io`
- Run `sudo systemctl status docker` to see if it is running
- Run `sudo usermod -aG docker ubuntu` to have permssions to execute docker commands
- log out and then log back in

