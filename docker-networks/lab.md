### Simple Lab to Practice Docker Networking 🚀

  01. Launch an EC2 instance (Ubuntu)
    - `Launch Instances > Name: demo-server-docker > Image: Ubuntu > Instance Type: t3.micro > Key Pair > Launch`
  02. SSH into your EC2 instance
    - `ssh -i "key-pair.pem" ubuntu@<public-ip-addr>`
  03. Install Docker
    - `sudo apt update && sudo apt install -y docker.io`
  04. Check if system status of Docker
    - `sudo systemctl status docker`
  05. Grant permissions to non-root user, exit instance and re-enter. Test if docker works!
    - `sudo usermod -aG docker ubuntu`
    - `docker ps` or `docker images`
  06. Create two containers using nginx image 
    - `docker run -itd --rm --name mahomes nginx:latest` & `docker run -itd --rm --name lamar nginx:latest`
  07. Inspect the network of both containers
    - `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mahomes lamar`
    - Output for mahomes: `172.17.0.2`
    - Output for lamar: `172.17.0.3`
  08. Check the gateway for one of the containers
    - `docker inspect -f '{{range .NetworkSettings.Network}}{{.Gateway}}{end}' mahomes lamar`
    - Output: `172.17.0.1` which is the bridge (docker0) IP Address
  09. Exec into one mahomes container and curl to lamar container with its IP Address
    - `docker exec -it mahomes sh`
    - `curl 172.17.0.3`
    - Output: `Welcome to nginx! If you see this page, the nginx web server is successfully installed...`
  10. In the `mahomes` container install the ping command and ping `lamar` container
    - `apt update && apt install -y iputils-ping`
    - `ping 172.17.0.3`
    - Output: `64 bytes from` IP Address
  11. Check route table inside the container you exec'd into:
    - `ip route`
  12. Create a custom network
    - `docker network create custom_bridge`
  13. Create a container with custom network
    - `docker run -itd --rm --name allen --network=custom_bridge nginx:latest`
  14. Now inspect the container and see what you find
    - `docker inspect -f '{{range .NetworkSettings.Network}}{{.IPAddress}}{end}' allen`
    - Output: 172.18.0.2
  15. Inspect the gateway of `allen` container within the user-defined bridge:
    - `docker inspect -f '{{range .NetworkSettings.Network}}{{.Gateway}}{end}' allen`
    - Output: `172.18.0.1`