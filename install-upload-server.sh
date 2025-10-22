#!/bin/bash
echo "Installing ESSIEM MT5 Upload Server..."
cd /opt
git clone https://github.com/ESSIEM1/ESSIEM_SYSTEMS-MT5-UploadServer.git
cd ESSIEM_SYSTEMS-MT5-UploadServer
docker build -t essiem-mt5-upload-server -f Dockerfile-ea-upload .
docker run -d --name essiem-upload -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock --restart unless-stopped essiem-mt5-upload-server
echo "✅ ESSIEM Upload Server installed!"
echo "🌐 Access at: http://$(hostname -I | awk '{print $1}'):8080"
