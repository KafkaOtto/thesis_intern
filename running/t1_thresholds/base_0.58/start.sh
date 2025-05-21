#!/bin/bash

LOGFILE="start.log"

echo "Running db initialization.sh..." >> "$LOGFILE"
sh db_init.sh >> "$LOGFILE" 2>&1

echo "Running pod initialization..." >> "$LOGFILE"
sh install.sh >> "$LOGFILE" 2>&1