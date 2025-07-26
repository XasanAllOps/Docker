## Multi-Stage Builds (Docker)

- The idea behind multi-stage builds is to keep our docker images lean, secure and production ready.
- I will use the Dockerfile I created for a simple project and improve it by using multi-stage builds
- The goal is to keep only what's neccessary to run our container eficiently

### Original Dockerfile vs Multi-Stage Dockerfile

```dockerfile
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│           Original Dockerfile                 │           Multi-Stage Dockerfile              │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────┐  │ ┌─────────────────────────────┐               │
│ │             Base Image:                  │  │ │       Stage 1: Builder      │               │
│ │          python:3.13-slim                │  │ │ ┌─────────────────────────┐ │               │
│ └──────────────────────────────────────────┘  │ │ │ Base Image: python:3.13 │ │               │
│                    │                          │ │ │                         │ │               │
│                    ▼                          │ │ │ WORKDIR /app            │ │               │
│ ┌──────────────────────────────────────────┐  │ │ │ COPY requirements.txt   │ │               │
│ │              WORKDIR /app                │  │ │ │ RUN pip install -r ...  │ │               │
│ │    (Sets working directory inside image) │  │ │ │ (Installs deps into     │ │               │
│ └──────────────────────────────────────────┘  │ │ │  /install folder)       │ │               │
│                    │                          │ │ └─────────────────────────┘ │               │
│                    ▼                          │ └───────────────┬─────────────┘               │
│ ┌──────────────────────────────────────────┐  │                 │ COPY --from=builder         │
│ │          COPY requirements.txt           │  │                 ▼                             │
│ │    (Copies dependencies list into image) │  │ ┌─────────────────────────────┐               │
│ └──────────────────────────────────────────┘  │ │      Stage 2: Final Image   │               │
│                    │                          │ │ ┌─────────────────────────┐ │               │
│                    ▼                          │ │ │ Base Image: python:3.13 │ │               │
│ ┌──────────────────────────────────────────┐  │ │ │                         │ │               │
│ │ RUN pip install --no-cache-dir -r re.txt │  │ │ │ WORKDIR /app            │ │               │
│ │ (Installs Python packages inside image)  │  │ │ │ COPY /install /usr/local│ │               │
│ └──────────────────────────────────────────┘  │ │ │ COPY devops/ (app code) │ │               │
│                    │                          │ │ │ EXPOSE 8000             │ │               │
│                    ▼                          │ │ │ CMD to run Django       │ │               │
│ ┌──────────────────────────────────────────┐  │ │ └─────────────────────────┘ │               │
│ │              COPY devops/                │  │ └─────────────────────────────┘               │
│ │         (Copies Django app code)         │  │                                               │
│ └──────────────────────────────────────────┘  │                                               │
│                    │                          │                                               │
│                    ▼                          │                                               │
│ ┌──────────────────────────────────────────┐  │                                               │
│ │               EXPOSE 8000                │  │                                               │
│ │     (Declare port container listens on)  │  │                                               │
│ └──────────────────────────────────────────┘  │                                               │
│                    │                          │                                               │
│                    ▼                          │                                               │
│ ┌──────────────────────────────────────────┐  │                                               │
│ │ CMD ["python", "manage.py",              │  │                                               │
│ │      "runserver", "0.0.0.0:8000"]        │  │                                               │
│ │     (Starts Django development server)   │  │                                               │
│ └──────────────────────────────────────────┘  │                                               │
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```