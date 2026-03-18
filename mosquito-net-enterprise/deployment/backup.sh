#!/bin/bash
DATE=$(date +%F)
mkdir -p /opt/mosquito/backups
cp /opt/mosquito/server/mosquito.db /opt/mosquito/backups/mosquito_$DATE.db