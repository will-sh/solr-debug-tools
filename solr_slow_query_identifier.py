import re
from datetime import datetime

def extract_and_sort_log_entries(file_content):
    log_entries = []  # Create a list to store log entries

    # Process each line from the file content
    for line in file_content.splitlines():
        # Regular expressions to extract QTime, timestamp, and params
        qtime_match = re.search(r'QTime=(\d+)', line)
        timestamp_match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)', line)
        params_match = re.search(r'params=({.*?})', line)

        # Extract QTime, timestamp, and params if found
        qtime = int(qtime_match.group(1)) if qtime_match else None
        timestamp = timestamp_match.group(1) if timestamp_match else None
        params = params_match.group(1) if params_match else None

        # Create a tuple for sorting
        log_entry = (qtime, timestamp, params, line.strip())

        # Append the log entry to the list
        log_entries.append(log_entry)

    # Sort by reverse order of QTime
    log_entries.sort(reverse=True)

    # Return the sorted log entries
    return log_entries

def search_logs_by_filters(log_entries, start_timestamp, end_timestamp, min_qtime=None):
    # Filter log entries within the specified timestamp range
    filtered_entries = [entry for entry in log_entries if start_timestamp <= entry[1] <= end_timestamp]

    # Apply additional filter for QTime if specified
    if min_qtime is not None:
        filtered_entries = [entry for entry in filtered_entries if entry[0] is not None and entry[0] >= min_qtime]

    return filtered_entries

def find_file_time_range(file_content):
    lines = file_content.splitlines()

    first_line = lines[0]
    last_line = lines[-1]

    first_timestamp_match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)', first_line)
    last_timestamp_match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)', last_line)

    if first_timestamp_match and last_timestamp_match:
        first_timestamp = first_timestamp_match.group(1)
        last_timestamp = last_timestamp_match.group(1)
        return first_timestamp, last_timestamp
    else:
        return None, None

# File path to the log file
log_file_path = 'slow_requests.log'

# Read the file content
with open(log_file_path, 'r') as file:
    file_content = file.read()

# Call the function to identify the time range of the file
start_time, end_time = find_file_time_range(file_content)

if start_time and end_time:
    print(f"Input file time range: {start_time} to {end_time}\n")

# Function to validate timestamps
def is_valid_timestamp(timestamp):
    try:
       datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
       return True
    except ValueError:
        try:
            datetime.strptime(timestamp, '%Y-%m-%d')
            return True
        except ValueError:
            return False
# Function to validate QTime
def is_valid_qtime(qtime):
    return qtime.isdigit() and int(qtime) >= 0

def is_valid_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
# Allow user input for start_timestamp, end_timestamp, and min_qtime with error handling
while True:
    start_timestamp = input("Enter start timestamp (e.g., '2022-12-01 00:00:00.000' or '2022-12-01'): ")
    end_timestamp = input("Enter end timestamp (e.g., '2022-12-31 23:59:59.999' or '2022-12-31'): ")
    min_qtime_str = input("Enter minimum QTime (leave empty to skip): ")

    if is_valid_timestamp(start_timestamp) and is_valid_timestamp(end_timestamp):
        # Validate start_timestamp and end_timestamp as dates
        start_date = start_timestamp.split()[0]
        end_date = end_timestamp.split()[0]
        if not is_valid_date(start_date) or not is_valid_date(end_date):
            print("Invalid date format in timestamps.")
            continue

        # Validate month (1-12) and day (1-31) in timestamps
        start_month, start_day = map(int, start_date.split('-')[1:])
        end_month, end_day = map(int, end_date.split('-')[1:])
        if (start_month < 1 or start_month > 12 or start_day < 1 or start_day > 31 or
            end_month < 1 or end_month > 12 or end_day < 1 or end_day > 31):
            print("Invalid month or day in timestamps.")
            continue

        min_qtime = int(min_qtime_str) if min_qtime_str and is_valid_qtime(min_qtime_str) else None
        break
    else:
        print("Invalid timestamp format. Please input calendar time follow this format: 'YYYY-MM-DD HH:MM:SS.sss' or 'YYYY-MM-DD'")
        print("QTime should be a positive integer.")

# Call the function to extract and sort log entries
sorted_log_entries = extract_and_sort_log_entries(file_content)

# Search logs using user-specified filters
filtered_entries = search_logs_by_filters(sorted_log_entries, start_timestamp, end_timestamp, min_qtime)

# Print the filtered log entries
for entry in filtered_entries:
    qtime, timestamp, params, log_message = entry
    print("QTime:", qtime)
    print("Timestamp:", timestamp)
    print("Params:", params)
    print("Log Message:", log_message)
    print("=" * 50)  # Separate entries with a line of equal signs
