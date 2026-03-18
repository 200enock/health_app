# Architecture
- Unified PWA + Mobile Wrappers
- Backend API Python
- Offline-first
- Dashboard with Charts & Maps
- AI Prediction

┌───────────────────────────────────────────────────────────┐
│                       SYSTEM ARCHITECTURE                  │
└───────────────────────────────────────────────────────────┘

                        ┌───────────────┐
                        │   Clients     │
                        │ (Web & PWA)   │
                        └───────┬───────┘
                                │
                                ▼
                        ┌───────────────┐
                        │   Nginx / API │
                        └───────┬───────┘
                                │
                                ▼
                ┌───────────────────────────────────┐
                │            Python Backend          │
                │  (REST API + Sync + Prediction)    │
                └──────────┬───────────┬──────────────┘
                           │           │
           ┌───────────────┘           └───────────────┐
           ▼                                               ▼
┌─────────────────────────┐                     ┌─────────────────────────┐
│       SQLite/Postgres    │                     │      Background Jobs    │
│  (Patients, Dist., Logs) │                     │  Sync / Prediction / AI │
└─────────────────────────┘                     └─────────────────────────┘
           │                                               │
           └──────────────────────┬────────────────────────┘
                                  ▼
                        ┌─────────────────────────┐
                        │   Dashboard/Reports     │
                        │   Charts & Maps (GIS)   │
                        └─────────────────────────┘

Mobile Flow:

    PWA (Offline-first) → Install on device
           ↓
    Android/iOS Capacitor Wrappers
           ↓
    Build APK / IPA

🧠 Explanation of the Diagram
Clients

PWA Browser — Desktop & Mobile

Android APK — Wrapped with Capacitor

iOS IPA — Wrapped with Capacitor

All interact through:

➡ Nginx API Gateway

Handles HTTPS

Routes to backend

Can load balance multiple instances

Backend

Python API

Patient registration

Net distribution

AI malaria risk

Database

SQLite (development)

PostgreSQL (production)

Background Jobs

Sync engine

Prediction tasks

Dashboard

Uses Chart.js and Leaflet (GIS maps)

Displays:

Distribution counts

Risk heatmaps

District analytics
