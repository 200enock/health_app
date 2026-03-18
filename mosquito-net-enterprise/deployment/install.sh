#!/bin/bash
sudo apt update
sudo apt install python3 python3-pip nginx certbot -y
pip3 install -r /opt/mosquito/server/requirements.txt
sudo cp -r mosquito-net-enterprise/* /opt/mosquito/
sudo systemctl daemon-reload
sudo systemctl enable mosquito
sudo systemctl start mosquito
sudo cp deployment/nginx.conf /etc/nginx/sites-available/mosquito
sudo ln -s /etc/nginx/sites-available/mosquito /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx