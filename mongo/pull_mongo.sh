#!/bin/bash

CURRENTDATE=$(date +"%Y-%m-%d-%H-%M")

echo "Current Date and Time is: ${CURRENTDATE}"

# Server-Hostname
SERVER="www2"

# Benutzername für die SSH-Verbindung
USERNAME="flask-reader"

ARCHIVE="user_backup_${CURRENTDATE}"

# Dump auf dem Remote-Server. Doppelte Anführungszeichen: ${ARCHIVE} wird
# lokal expandiert, sodass der gleiche Dateiname für scp/mongorestore gilt.
ssh $USERNAME@$SERVER "cd mi-user/backup && mongodump --db user --archive=${ARCHIVE}"
scp $USERNAME@$SERVER:~/mi-user/backup/${ARCHIVE} .
mongorestore --drop --archive=${ARCHIVE}
