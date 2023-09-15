import re

def extract_and_sort_log_entries(file_path):
    log_entries = []  # Create a list to store log entries

    # Open the log file and process each line
    with open(file_path, 'r') as file:
        for line in file:
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

# File path to the log file
log_file_path = 'slow_requests.log'

# Call the function to extract and sort log entries
sorted_log_entries = extract_and_sort_log_entries(log_file_path)

# Allow user input for start_timestamp, end_timestamp, and min_qtime
start_timestamp = input("Enter start timestamp (e.g., '2022-12-01 00:00:00.000'): ")
end_timestamp = input("Enter end timestamp (e.g., '2022-12-31 23:59:59.999'): ")
min_qtime_str = input("Enter minimum QTime (leave empty to skip): ")

# Convert min_qtime to an integer if provided
min_qtime = int(min_qtime_str) if min_qtime_str else None

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

