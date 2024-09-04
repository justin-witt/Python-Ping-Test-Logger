Ping Script

This Python script allows you to ping an IP address or DNS name and logs the results to a file on your desktop. It supports command-line arguments to specify the target address and can validate both IP addresses and DNS names.

Requirements

1. Python 3.x: This script requires Python 3.x. You can download and install it from the official Python website.
2. No additional Python libraries: The script uses only the standard library modules included with Python.

Features

1. Ping IP or DNS: Ability to ping both IP addresses and DNS names.
2. Custom Logging: Logs the date, time, and response time to a file on the desktop.
3. Command-Line Argument: Use the -target flag to specify the target directly from the command line.
4. Interactive Mode: Prompts for input if no target is provided via command-line argument.

Installation

1. Ensure Python is Installed: This script requires Python 3.x. Download and install it from the official Python website.
2. Copy the script to your local machine.

Usage

1. Command-Line Argument: Run the script with the -target flag to specify the IP address or DNS name.
   - python script_name.py -target "your_target"
   Replace script_name.py with the actual name of your Python script and your_target with the IP address or DNS name you want to ping.
2. Shortcut Argument: You can also use the -t flag as a shortcut for -target.
   - python script_name.py -t "your_target"
3. Interactive Mode: If the -target flag is not used, the script will prompt you to enter a valid IP address or DNS name.

Output

1. Successful Ping: The log file on your desktop will include entries with the date, time, and response time. The format will be similar to:
   - 09:05:22_123 - Ping to 192.168.1.1 was successful with a response time of 25 ms.
2. Failed Ping: If the ping fails, the log will note the failure.
   - 09:05:22_123 - Ping to 192.168.1.1 failed.

Variables (edited in script)

LOG_FILENAME: Defines the name of the log file. By default, it is set to ping_log.txt.

DATE_FORMAT: Specifies the format for timestamps in the log file. Default is %m:%d:%y::%H:%M:%S.

DESKTOP_PATH: The directory where the log file is saved, defaulting to the user's Desktop. Change with caution.

SECONDS_BETWEEN_PING: Time interval (in seconds) between consecutive pings. Default is 1 second.

MAX_LOG_FILE_SIZE_MB: Maximum size of the log file before rotation, set to 10 MB by default.

MAX_NUMBER_LOG_FILES: Maximum number of log files to store.