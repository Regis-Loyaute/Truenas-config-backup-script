import os
import subprocess
import requests
import schedule
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# USER CONFIGURABLE VARIABLES
server_url = os.environ['SERVER_URL']
api_key = os.environ['API_KEY']
sec_seed = os.environ['SEC_SEED']
backuploc = os.environ['BACKUPLOC']
max_nr_of_files = int(os.environ['MAXNR_OF_FILES'])
scheduled_time = os.environ['SCHEDULED_TIME']  # Time to run the job

# Set directory for backups
backup_main_dir = backuploc
os.makedirs(backup_main_dir, exist_ok=True)

def backup():
    # Use appropriate extension if we are exporting the secret seed
    file_ext = "tar" if sec_seed.lower() == "true" else "db"

    # Generate file name
    file_name = f"{subprocess.check_output('hostname').decode().strip()}-TrueNAS-{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"

    response = requests.post(
        f"{server_url}/api/v2.0/config/save",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "*/*",
            "Content-Type": "application/json"
        },
        json={"secretseed": sec_seed.lower() == "true"},
        verify=False,  # Bypass SSL certificate verification
        stream=True,  # Stream the response content
    )

    with open(os.path.join(backup_main_dir, file_name), "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # The next section checks for and deletes old backups
    if max_nr_of_files != 0:
        file_list = [f for f in os.listdir(backup_main_dir) if os.path.isfile(os.path.join(backup_main_dir, f))]
        nr_of_files = len(file_list)

        if max_nr_of_files < nr_of_files:
            n_files_to_remove = nr_of_files - max_nr_of_files
            file_list.sort(key=lambda f: os.path.getctime(os.path.join(backup_main_dir, f)))

            for i in range(n_files_to_remove):
                file_to_remove = file_list[i]
                os.remove(os.path.join(backup_main_dir, file_to_remove))

# Schedule the backup function
schedule.every().day.at(scheduled_time).do(backup)

# Print message before starting the backup
print("Starting backup...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

# Print message after the backup is complete
print("Backup completed.")
