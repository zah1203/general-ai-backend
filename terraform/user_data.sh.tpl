#!/bin/bash
set -e

dnf update -y
dnf install -y docker git

systemctl enable docker
systemctl start docker

cd /opt
rm -rf genorax-ai-backend
git clone ${github_repo_url} genorax-ai-backend

cd genorax-ai-backend

docker build -t genorax-ai-backend .
docker rm -f genorax-ai-backend || true
docker run -d \
  --name genorax-ai-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  genorax-ai-backend
