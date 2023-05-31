The script allows for automated, daily backups of a TrueNAS system's configuration, with the potential inclusion of sensitive encryption-related data, and manages the deletion of old backups.


The backup() function in the script is used to generate a backup of the TrueNAS system's configuration.

The configuration data is fetched by making an API call to the TrueNAS server, specifically to the /api/v2.0/config/save endpoint.

If sec_seed is true, the secret seed (likely related to encryption keys) is included in the configuration backup. The backed-up data is received as a response from the API call.

The response data (the backup) is then written into a file in a specified location. The file naming scheme reflects the system hostname, the date and time of the backup, and the type of backup (whether it includes the secret seed or not). This backup file can be used to restore the TrueNAS system configuration if needed.

The script also manages old backup files. If the number of backup files in the directory exceeds the MAXNR_OF_FILES environment variable, it will delete the oldest backup files until the limit is met.

The backup() function is scheduled to run at a specific time each day (determined by the SCHEDULED_TIME environment variable).