import os
import csv

# Define the root directory and log file
root_dir = r"J:\\SR116711\X_by name"  # Change to your desired directory
log_file = r"C:\Users\SHENGTAOHOU\Desktop\inaccessible_files_log.csv"

# Initialize the log file and write the CSV header
with open(log_file, 'w', newline='', encoding='utf-8') as log:
    csv_writer = csv.writer(log)
    csv_writer.writerow(["Type", "Path", "Message"])

# Function to log messages in CSV format
def log_message(type, path, message):
    with open(log_file, 'a', newline='', encoding='utf-8') as log:
        csv_writer = csv.writer(log)
        csv_writer.writerow([type, path, message])
    print(f"{type}: {path} | {message}")

# Initialize counters
inaccessible_files = 0
inaccessible_folders = 0

# Traverse the directory
for root, dirs, files in os.walk(root_dir):
    # Check folder access
    for dir_name in dirs:
        folder_path = os.path.join(root, dir_name)
        try:
            os.listdir(folder_path)
        except PermissionError as e:
            log_message("Folder", folder_path, "Permission Denied")
            inaccessible_folders += 1

    # Check file access
    for file_name in files:
        file_path = os.path.join(root, file_name)
        try:
            with open(file_path, 'rb'):
                pass
        except PermissionError as e:
            log_message("File", file_path, "Permission Denied")
            inaccessible_files += 1

# Log the summary
log_message("Summary", "", f"Total inaccessible folders: {inaccessible_folders}")
log_message("Summary", "", f"Total inaccessible files: {inaccessible_files}")

print("Traversal completed.")
