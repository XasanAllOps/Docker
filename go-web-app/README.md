[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=black)](#)

## Containerizing a Simple Golang Application with Docker

I wanted demonstrate how to containerise a basic Go application using a simple Dockerfile, and later with multi-stage-distroless builds

### Simple Dockerfile (No Multi-Stage/No Distroless/No Ports)

### Check Golang Version

  - `go version` = Output: `go version go1.20.6 darwin/amd64`
  - The Go programming language is an open source project to make programmers more productive (https://go.dev/doc/)

### Dockerfile (Breakdown)

```sql
FROM golang:1.21
WORKDIR /app
COPY . .
RUN go build -o app
CMD ["./app"]
```

- `FROM golang:1.21`: Uses the official Go image pinned to a specific version for stability

- `WORKDIR /app`: Sets the working directory inside the container & prevents hardcoding full paths
- `COPY . .`: 
  - Copy everything from the current directory on the host to the container directory (/app) into the current working directory inside the container (/app) 🐳 📦
  - Can also do `COPY . /app` as well but the otherway is more simpler

- `RUN go build -o app`: 
  - Why not `go run .`?
    - `go run .`: Compiles the code into a temporary binary and runs it directly. It does not create a persistent binary file (like ./app)
    - `go run .`: Requires Go to be installed in the final image (not wise/bloated). For local dev it's good.
    - `go build -o app`: Standard way for Docker. Produces a standalone binary (app) that you can copy into a smaller image. Repeatable, optimised, and portable build + multi-stage Docker build + distroless

- CMD `["./app"]`: 
  - Tells Docker what to run when the container starts
  - The image contains everything built including the compiled Go binary (app)
  - Docker looks inside the image, goes to `/app` and executes the app binary.

### Running It on AWS EC2 (Ubuntu)

- Launch an Ubuntu EC2 Instance
- SSH into your EC2 (`ssh -i "<KEY>" ubuntu@<ec2-public-key>`)
- Run `sudo apt update && sudo apt install -y docker.io`
- Run `sudo systemctl status docker` to check Docker status 🟢
- Run `sudo usermod -aG docker ubuntu` to add ubuntu user to Docker group
- Log out and then log back in 
- Clone the repository containing the project: `git clone https://github.com/<username>/<repo>.git`
- `cd` to project directory
- Run `docker build -t go-app .`
- Run `docker run --rm go-app`
- It will return `We are go-liveeeeeee 🎉`

## Optimising with Multi-Stage Builds and Distroless Images (Smaller, Safer Containers)