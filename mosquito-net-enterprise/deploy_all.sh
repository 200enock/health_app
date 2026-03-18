#!/bin/bash

# =============================
# Mosquito Net Enterprise System
# Quickstart Deployment Script
# =============================

# Exit on error
set -e

echo "🦟 Starting deployment of Mosquito Net Enterprise System"

# 1️⃣ Update & install dependencies
echo "Installing system packages..."
sudo apt update
sudo apt install -y python3 python3-pip nginx certbot unzip nodejs npm git

# 2️⃣ Copy project to /opt/mosquito
echo "Setting up project folder..."
sudo mkdir -p /opt/mosquito
sudo cp -r mosquito-net-enterprise/* /opt/mosquito/

# 3️⃣ Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r /opt/mosquito/server/requirements.txt

# 4️⃣ Initialize Database
echo "Initializing SQLite database..."
python3 /opt/mosquito/server/db_init.py

# 5️⃣ Setup systemd service
echo "Setting up backend service..."
sudo cp /opt/mosquito/deployment/mosquito.service /etc/systemd/system/mosquito.service
sudo systemctl daemon-reload
sudo systemctl enable mosquito
sudo systemctl start mosquito
sudo systemctl status mosquito

# 6️⃣ Configure Nginx
echo "Configuring Nginx..."
sudo cp /opt/mosquito/deployment/nginx.conf /etc/nginx/sites-available/mosquito
sudo ln -sf /etc/nginx/sites-available/mosquito /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 7️⃣ Enable HTTPS with Certbot
echo "Enabling HTTPS..."
sudo certbot --nginx --non-interactive --agree-tos -m admin@yourdomain.com -d yourdomain.com

# 8️⃣ Setup daily database backup (cron)
echo "Setting up daily backups..."
(crontab -l ; echo "0 2 * * * /opt/mosquito/deployment/backup.sh") | crontab -

# 9️⃣ Prepare Android & iOS wrappers
echo "Preparing mobile wrappers..."
cd /opt/mosquito
npm install -g @capacitor/cli

# Android
echo "Copying Android wrapper..."
npx cap copy android
echo "Android wrapper ready (open android/ in Android Studio to build APK)"

# iOS (Mac only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Copying iOS wrapper..."
    npx cap copy ios
    echo "iOS wrapper ready (open ios/ in Xcode to build IPA)"
else
    echo "Skipping iOS wrapper (requires Mac for Xcode)"
fi

echo "✅ Mosquito Net Enterprise System deployed successfully!"
echo "Access PWA at: https://yourdomain.com/app.html"
echo "Dashboard at: https://yourdomain.com/dashboard.html"
echo "Android Studio: open /opt/mosquito/android"
echo "iOS Xcode: open /opt/mosquito/ios (on Mac)"

