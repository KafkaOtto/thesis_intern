#!/bin/bash

LOGFILE="start.log"

echo "Running db initialization.sh..." >> "$LOGFILE"
bash db_init.sh >> "$LOGFILE" 2>&1

echo "Running pod initialization..." >> "$LOGFILE"
bash install.sh >> "$LOGFILE" 2>&1