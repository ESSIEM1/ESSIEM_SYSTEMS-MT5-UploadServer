# ESSIEM SYSTEMS MT5 Upload Server

A web interface for uploading Expert Advisors, Indicators, and Scripts to MetaTrader 5 running in Docker.

## 🚀 Features

- Upload .ex5 files directly to MT5
- Clean web interface
- Automatic file placement in correct MQL5 directories
- Reset MT5 to factory state

## 📋 Requirements

- Docker
- [ESSIEM MT5 Terminal](https://github.com/ESSIEM1/essiem-mt5) container running

## 🛠 Installation

```bash
# Build the image
docker build -t essiem-mt5-upload-server .

# Run the container
docker run -d \
  --name essiem-upload \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  essiem-mt5-upload-server
