#!/bin/bash

LOGFILE="start.log"

echo "Running db initialization.sh..." >> "$LOGFILE"
./db_init.sh >> "$LOGFILE" 2>&1

echo "Running pod initialization..." >> "$LOGFILE"
./install.sh >> "$LOGFILE" 2>&1