# Cron Job Setup

To set up the cron job for data collection, follow these steps:

1. Open the terminal.
2. Edit the crontab file using the command `crontab -e`.
3. Add the following lines to the crontab file:

   ```bash
   # Run the data collection script every hour
   * * * * * home/user/bin/python3 /home/user/ISS-Data-Analysis/src/main.py >> /home/user/ISS-Data-Analysis/logs/main_log 2>&1

