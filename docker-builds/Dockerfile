# --- Stage 1: Build Environment 🏗️ 
# --- Install dependencies in an isolated /install directory

FROM python:3.13-slim AS builder 
# starts a temporary container called builder using a lightweight Python base image

WORKDIR /app
# creates and switches to the /app directory inside the container

COPY requirements.txt .
# copies requirements.txt file (from host) into /app in the container
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
# `pip install` will install all dependencies into /install
# `--prefix=/install`: this redirects the install output to /install/lib/python3.13/site-packages
# why use /install? In order to isolate all Python packages in one folder to copy later.


# --- Stage 2: Create final runtime image 🚀
# --- Lightweight, production-ready container with application + installed packages

FROM python:3.13-slim
# creates a new clean image, no build tools, no pip cache – just Python and whatever we copy into it

WORKDIR /app

COPY --from=builder /install /usr/local
# '--from=builder': "copy this from the container named builder"
# '/install': the folder in stage 1 containing all the installed Python packages
# 'usr/local': the standard directory where Python looks for installed packages in most environments
# In summary, "copy everything installed in STAGE 1 into the correct Python package location in the new image"

COPY devops/ .
# copies actual Django application code (settings.py, manage.py, etc) into /app

EXPOSE 8000
# declares that this container will listen on port 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]