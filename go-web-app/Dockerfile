FROM golang:1.21

# Set working directory inside the container
WORKDIR /app

COPY . .
# Copy everything from the current directory on the host 💻
# Into the current working directory inside the container (/app) 🐳 📦
# Can also do 'COPY . /app' as well but the otherway is more simpler

RUN go build -o app
# 'go run .': Compiles the code into a temporary binary and runs it directly. It does not create a persistent binary file (like ./app)
# 'go run .': requires Go to be installed in the final image (not wise/bloated). For local dev it's good.
# 'go build -o app': Standard way for Docker. Produces a standalone binary (app) that you can copy into a smaller image. Repeatable, optimised, and portable build + multi-stage Docker build + distroless

CMD ["./app"]

