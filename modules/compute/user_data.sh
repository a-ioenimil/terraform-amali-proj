#!/bin/bash
set -e

apt-get update -y
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

mkdir -p /var/lib/phpmyadmin/sessions
chmod 777 /var/lib/phpmyadmin/sessions

until docker info > /dev/null 2>&1; do
  sleep 1
done

docker run -d \
  --name phpmyadmin \
  --restart always \
  -p 80:80 \
  -e "PMA_HOST=${rds_endpoint}" \
  -e "PMA_PORT=3306" \
  -e "PMA_ARBITRARY=0" \
  -e "PMA_ABSOLUTE_URI=http://${alb_dns_name}/" \
  -v "/var/lib/phpmyadmin/sessions:/sessions:rw" \
  phpmyadmin:latest

sleep 30
