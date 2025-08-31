[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=black)](#)

## Docker Networking

### 🌉 Bridge Network (Default Network)

The Bridge network is the default network for Docker containers. It creates an isolated virtual network inside your host machine. Containers on this network can communicate with each other and be exposed to the host network via port mapping (`-p`).

### Components

- Host Machine: Has its own network stack.
- Docker Engine: The main service that manages containers.
- Linux Bridge (`docker0`): A virtual bridge created by Docker that acts as a _software switch_
- `veth`: Virtual Ethernet interfaces that link each container to `docker0`. Each container gets its own IP address.

### How It Works

1. Docker starts and creates `docker0` (a virtual Linux bridge).
2. Every container on the bridge network:
   - Gets a `veth` pair (a virtual Ethernet link).
   - The container-side interface `eth0` connects to `docker0` via the host-side `veth`.
3. The `docker0` bridge routes container traffic and switches packets based on MAC/IP.
4. Docker assigns IP addresses to containers from the subnet `172.17.0.0/16` by default.


### How to Find a Container’s IP Address 

```zsh
# For containers on the default bridge network:
docker inspect -f '{{ .NetworkSettings.IPAddress }}' container_name

# Works with both bridge and user-defined networks:
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name

# Gateway IP:
docker inspect -f '{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' container_name

# Full network settings (manual lookup):
docker inspect container_name
```
### Bridge Network Diagram

```sql
      [ Host Network Stack ]
  (Your OS with IP, routes, etc.)
               |
         [docker0 bridge]
          IP: 172.17.0.1      
               |
    +----------+----------+
    |                     |
  [veth0]               [veth2]       ← host-side interfaces
    |                     |
  [eth0] in C1          [eth0] in C2  ← container-side interfaces
IP: 172.17.0.2       IP: 172.17.0.3
```

### User-Defined Network (Custom Network)

Creating your own bridge network using `docker network create` results in a new virtual bridge interface (`br-xxxx`) on the host. User-defined bridges offer the advantage of automatic container name-based DNS resolution, allowing containers to communicate using their names rather than IP addresses. Additionally, these networks are isolated at the network level from Docker’s default bridge (docker0), ensuring better security and separation. For these reasons, it is highly recommended to use user-defined networks for real-world Docker setups for manageability and scalability.

Steps to create a user-defined bridge:

1. Create a custom bridge:
  - `docker network create custom_bridge`

2. Run a container attached to it:
  - `docker run -itd --rm --name allen --network=custom_bridge nginx:latest`

3. Inspect the network:
  - `docker network inspect custom_bridge`

## Bridge & User-Defined Network Diagram 🤝

The diagram below shows how containers connect to different bridge networks in Docker:  
  - The default bridge (`docker0`)  
  - A user-defined bridge (`custom_bridge`)

```sql
                         [ Host Network Stack ]
                     (Your OS with IP, routes, etc.)
                                 |
          +----------------------+----------------------+
          |                                             |
   [ docker0 bridge ]                         [ custom_bridge ]
    IP: 172.17.0.1                              IP: 172.18.0.1
          |                                             |
   +------+-------+                             +---------------+
   |              |                             |               |
[veth0]         [veth2]                      [veth0]        (others..)
   |              |                             |
[eth0] in C1    [eth0] in C2                 [eth0] in C1
172.17.0.2      172.17.0.3                   172.18.0.2
```
🚫 Containers on different bridges **cannot communicate with each other by default**  
✅ Containers on user-defined bridges can communicate using DNS (`ping <container_name>`) instead of using the IP addressess
