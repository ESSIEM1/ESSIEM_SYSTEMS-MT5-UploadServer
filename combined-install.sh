#!/bin/bash
echo "=== ESSIEM SYSTEMS Complete MT5 Installation ==="

# Update system
apt update && apt upgrade -y && apt install curl sudo -y

# Install MT5 Terminal
echo "Installing MT5 Terminal..."
curl -s https://raw.githubusercontent.com/ESSIEM1/ESSIEM_SYSTEMS-MT5-Server/main/one-line-install-essiem.sh | bash

# Wait for MT5 to start
echo "Waiting for MT5 to start..."
sleep 30

# Install Upload Server
echo "Installing Upload Server..."
curl -s https://raw.githubusercontent.com/ESSIEM1/ESSIEM_SYSTEMS-MT5-UploadServer/main/install-upload-server.sh | bash

echo "=== Installation Complete ==="
echo "MT5 Terminal: https://$(hostname -I | awk '{print $1}'):6080/vnc.html"
echo "Upload Server: http://$(hostname -I | awk '{print $1}'):8080"
