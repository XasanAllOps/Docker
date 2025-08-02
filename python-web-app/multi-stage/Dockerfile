# --- Stage 1: Build Environment 🏗️ 

FROM python:3.13-slim AS builder 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Create final runtime image 🚀

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY devops/ .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]