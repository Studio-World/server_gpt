#!/bin/bash
# Start Watchdog Automation Agent

echo "Startando agent watchdog..."

python3 "$(dirname "$0")/watchdoger.py"