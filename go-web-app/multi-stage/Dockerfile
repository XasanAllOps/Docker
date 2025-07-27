# --- Stage 1: Build Environment 🏗️ 
FROM golang:1.21 AS builder

WORKDIR /app

COPY . .

RUN CGO_ENABLED=0 go build -o app

# --- Stage 2: Lightweight Distroless final image 🚀

FROM scratch

WORKDIR /app

COPY --from=builder /app/app .

CMD ["./app"]