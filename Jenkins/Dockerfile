# Use the official Jenkins LTS image (Debian-based)
FROM jenkins/jenkins:lts

# Switch to root to install Docker
USER root

# Install Docker CLI + Compose plugin from Docker's official repo
RUN apt-get update && \
    apt-get install -y docker.io && \  
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

# Switch back to Jenkins user
USER jenkins
