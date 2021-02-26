#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Make messages from the Python script appear in the docker-compose log as they're printed.
export PYTHONUNBUFFERED=1

# Start the run-once job.
echo "Running initial Q&A API fetch."
./main.py

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID|PYTHONUNBUFFERED' > /container.env

# Set up a cron schedule to update the generated JSON files (every day at midnight).
echo "SHELL=/bin/bash
BASH_ENV=/container.env
0 0 * * * /usr/bin/env python3 -u /app/main.py >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
# Display output from cron.
touch /var/log/cron.log
cron -f & tail -f /var/log/cron.log
