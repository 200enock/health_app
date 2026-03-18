# Mosquito Net Enterprise System
Combined desktop & mobile PWA with Android/iOS builds ready.

🦟 Mosquito Net Enterprise System – Admin Cheatsheet & Deployment Flow
1️⃣ Deployment Flow Diagram
                ┌────────────────────┐
                │  Prepare Server     │
                │ (Ubuntu/Debian)     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Copy Project Files  │
                │ to /opt/mosquito    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Install Dependencies│
                │ Python, Nginx, Node │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Initialize DB       │
                │ sqlite3 / db_init.py│
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Backend Service     │
                │ systemd mosquito    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Nginx Configuration │
                │ + Certbot HTTPS     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ PWA Available       │
                │ https://domain/app │
                └─────────┬──────────┘
                          │
      ┌───────────────────┴───────────────────┐
      ▼                                       ▼
┌───────────────┐                       ┌───────────────┐
│ Mobile Android│                       │ Mobile iOS    │
│ npx cap copy  │                       │ npx cap copy  │
│ android → APK │                       │ ios → IPA     │
└───────────────┘                       └───────────────┘
2️⃣ Quick Admin Cheatsheet
Server Management
Task	Command
Start backend	sudo systemctl start mosquito
Stop backend	sudo systemctl stop mosquito
Restart backend	sudo systemctl restart mosquito
Check backend status	sudo systemctl status mosquito
Backup database	bash /opt/mosquito/deployment/backup.sh
Schedule daily backup	crontab -e → add 0 2 * * * /opt/mosquito/deployment/backup.sh
Nginx & HTTPS
Task	Command
Test config	sudo nginx -t
Restart Nginx	sudo systemctl restart nginx
Enable HTTPS	sudo certbot --nginx
Mobile App
Platform	Command / Steps
Android APK	cd /opt/mosquito → npx cap copy android → open android/ in Android Studio → Build APK
iOS IPA	cd /opt/mosquito → npx cap copy ios → open ios/ in Xcode → Archive → Export IPA
PWA Access

Desktop / Mobile: https://yourdomain.com/app.html

Dashboard: https://yourdomain.com/dashboard.html

3️⃣ Usage Flow for Admins

Login using role-based account.

Register patients & enter NIN/household data.

Distribute nets; system calculates AI malaria risk.

View dashboard for:

Net distribution charts

Map of high-risk areas

Reports & statistics

Export or backup data regularly.

Update system:

Update client/ files → npx cap copy android/ios

Restart systemd service → sudo systemctl restart mosquito

4️⃣ Tips for Nationwide Deployment

Use HTTPS and domain/subdomain for each region if needed.

Automate database backup with cron.

Monitor logs: /var/log/syslog + mosquito.log (optional).

Push PWA updates → mobile apps automatically sync with npx cap copy.

Use role-based access for district-level admins.

✅ Result:
Your admins can now deploy, manage, and scale the Mosquito Net System nationwide without touching the code.
It’s fully enterprise-ready, mobile-ready, offline-capable, and AI-enhanced.
