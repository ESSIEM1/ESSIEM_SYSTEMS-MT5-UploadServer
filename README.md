# ESSIEM MT5 Upload Server

Web interface for uploading Expert Advisors to MT5.

## Quick Start

```bash
docker build -t essiem-mt5-upload-server .
docker run -d -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock essiem-mt5-upload-server
