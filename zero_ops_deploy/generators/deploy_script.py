def generate_deploy_script(docker_username, image_name, port):
    return f"""#!/bin/bash

#Installing Docker on the EC2 instance
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
newgrp docker

#Pulling and running the container 
docker pull {docker_username}/{image_name}:latest
docker run -d -p {port}:{port} {docker_username}/{image_name}:latest
"""
