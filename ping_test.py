import os
import argparse
import logging
import subprocess
import time
import re
from logging.handlers import RotatingFileHandler

# Configurable variables
DATE_FORMAT = '%m:%d:%y::%H:%M:%S' ###!!!CHANGE WITH CAUTION!!!###
# Adding date/time to file name will cause it make a new set of files every time the script is reset
# so if you stop running your test and start it again you will ended up with the exisiting files
# however I did not want to lose the format to add the date/time or whatever to the front so it is in the comment below
LOG_FILENAME = "ping_log.txt" # time.strftime(DATE_FORMAT.replace(':','_'), time.localtime()) + "_" + 
DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') # THIS IS THE LOG FILE OUTPUT FOLDER ADJUST WITH CAUTION
LOG_FILE_PATH = os.path.join(DESKTOP_PATH, LOG_FILENAME) # DO NOT TOUCH PYTHON MAGIC
SECONDS_BETWEEN_PING = 1 # Time to wait between sending pings. 

# Size limit variables
MAX_LOG_FILE_SIZE_MB = 10  # Max log file size in megabytes
MAX_LOG_FILE_SIZE_BYTES = MAX_LOG_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
MAX_NUMBER_LOG_FILES = 5 # Number of log files to keep once size limit is reached. I have no idea if this works.


# Custom logging formatter to include milliseconds
class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime(self.default_time_format, ct)
            s = "%s,%03d" % (t, record.msecs)
        return s

# Set up logging
handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=MAX_LOG_FILE_SIZE_BYTES,
    backupCount=MAX_NUMBER_LOG_FILES # Number of backup files to keep
)
handler.setFormatter(CustomFormatter('%(asctime)s_%(msecs)03d - %(message)s', datefmt=DATE_FORMAT))
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
)

def is_valid_ip_or_dns(target):
    """Validate the IP address format or DNS name."""
    ip_pattern = re.compile( # regex magic
        r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return ip_pattern.match(target) or (len(target) > 0 and not target[0].isdigit())

def ping_ip_or_dns(target):
    """Ping the IP address or DNS name and log the response time."""
    try:
        output = subprocess.check_output(["ping", "-n", "1", target], stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Extract the time from the ping output (time=x ms)
        match = re.search(r'time[=<]\s*(\d+)\s*ms', output) #more regex magic
        if match:
            response_time = match.group(1)
            logging.info(f"Ping to {target} was successful with a response time of {response_time} ms.")
            print(f"Ping to {target} was successful with a response time of {response_time} ms.")
        else:
            logging.info(f"Ping to {target} was successful, but no response time found.")
            print(f"Ping to {target} was successful, but no response time found.")
        
    except subprocess.CalledProcessError as e:
        logging.warning(f"Ping to {target} failed.")
        print(f"Ping to {target} failed.")

def main():
    # handle if user passes in target as argument/flag
    parser = argparse.ArgumentParser(description="Ping an IP address or DNS name.")
    parser.add_argument('-target', '-t', type=str, help='Target IP address or DNS name to ping')
    args = parser.parse_args()

    target = args.target

    # prompt user for target
    if not target:
        while True:
            target = input("Please enter a valid IP address or DNS name: ")
            if is_valid_ip_or_dns(target):
                break
            print("Invalid IP address or DNS name. Please try again.")

    # perform test
    print(f"Pinging {target}... Press Ctrl + C to stop.")
    try:
        while True:
            ping_ip_or_dns(target)
            time.sleep(SECONDS_BETWEEN_PING)
    except KeyboardInterrupt:
        print("\nPinging stopped.")

# quirky python to make me look smart
if __name__ == "__main__":
    main()
