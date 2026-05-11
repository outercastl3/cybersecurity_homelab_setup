#!/bin/bash
set -e

# Dependencies
apt update
apt install sudo curl gnupg ca-certificates -y

# sudo group
usermod -aG sudo $USER

# Docker GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod 644 /etc/apt/keyrings/docker.gpg

# Add Docker repo
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/debian trixie stable" | \
tee /etc/apt/sources.list.d/docker.list

# Actual Docker install
apt update && apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
