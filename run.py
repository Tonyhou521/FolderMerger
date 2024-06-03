import os
import shutil
import csv
from datetime import datetime
import time

# Define the root directories
base_recovery_dir = r"J:\SR116711"
current_dir = r"*****************"

# Construct the recovery directory from the current directory
relative_path = os.path.relpath(current_dir, r"J:\\")
recovery_dir = os.path.join(base_recovery_dir, relative_path)

# Define the log file path
current_folder_name = os.path.basename(current_dir)
log_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'RecoveryLog')
log_file = os.path.join(log_folder, f"move_log_{current_folder_name}.csv")

# Initialize the log file and write the CSV header
with open(log_file, 'w', newline='', encoding='utf-8') as log:
    csv_writer = csv.writer(log)
    csv_writer.writerow(["Action", "Source File", "Destination File", "Message"])

# Function to log messages in CSV format
def log_message(action, src, dst, message):
    with open(log_file, 'a', newline='', encoding='utf-8') as log:
        csv_writer = csv.writer(log)
        csv_writer.writerow([action, src, dst, message])
    # Print concise log to terminal
    print(f"{action}: {message}")

# Initialize progress counter
folder_counter = 0
total_folders = 0
new_dirs_created = 0
files_failed_to_move = 0
files_protected_or_no_access = 0

# Count total folders for progress indicator
print("Counting total folders")

for root, dirs, files in os.walk(recovery_dir):
    total_folders += len(dirs)

print("Counting Completed.. Moving Initializing...")

# Function to check and create directories
def ensure_dir_exists(path):
    global new_dirs_created
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            new_dirs_created += 1
            log_message("Directory Created", "", path, "New directory created")
    except PermissionError as e:
        log_message("Permission Denied", "", path, str(e))
    except OSError as e:
        log_message("Failed", "", path, str(e))

# Function to move file with long path support
def move_file(src, dst):
    try:
        if len(src) > 260 or len(dst) > 260:
            src = r"\\?\{}".format(src)
            dst = r"\\?\{}".format(dst)
        shutil.move(src, dst)
        return True
    except PermissionError as e:
        log_message("Protected/No Access", src, dst, str(e))
        return False
    except OSError as e:
        log_message("Failed", src, dst, str(e))
        return False

# Throttle duration in seconds
throttle_duration = 0  # Adjust the sleep duration as needed

# Start timer
start_time = time.time()

# Loop through each first-level folder in the recovery directory
for root_recovery, dirs_recovery, files_recovery in os.walk(recovery_dir, topdown=True):
    for dir_name in dirs_recovery:
        dir_path = os.path.join(root_recovery, dir_name)
        try:
            os.listdir(dir_path)
        except PermissionError as e:
            log_message("Permission Denied", dir_path, "", "Cannot access directory")
            files_protected_or_no_access += 1
        except OSError as e:
            log_message("Failed", dir_path, "", str(e))
            files_failed_to_move += 1

    for file_name in files_recovery:
        recovery_file = os.path.join(root_recovery, file_name)
        relative_path = os.path.relpath(root_recovery, recovery_dir)
        current_file = os.path.join(current_dir, relative_path, file_name)

        # Ensure directory structure exists
        ensure_dir_exists(os.path.dirname(current_file))

        # Check if the file exists in the current directory
        if os.path.exists(current_file):
            try:
                recovery_mtime = os.path.getmtime(recovery_file)
                current_mtime = os.path.getmtime(current_file)

                if recovery_mtime > current_mtime:
                    # Recovery file is newer, move it
                    if move_file(recovery_file, current_file):
                        log_message("Moved", recovery_file, current_file, "Moved newer file")
                    else:
                        files_failed_to_move += 1
                elif recovery_mtime < current_mtime:
                    # Current file is newer, skip moving
                    log_message("Skipped", recovery_file, current_file, "Current is newer")
                else:
                    # Files have identical modification times, skip moving
                    log_message("Skipped", recovery_file, current_file, "Identical modification times")
            except PermissionError as e:
                log_message("Permission Denied", recovery_file, current_file, str(e))
                files_protected_or_no_access += 1
            except OSError as e:
                log_message("Failed", recovery_file, current_file, str(e))
                files_failed_to_move += 1
        else:
            # File does not exist in the current directory, move it
            try:
                if move_file(recovery_file, current_file):
                    log_message("Moved", recovery_file, current_file, "Moved file")
                else:
                    files_failed_to_move += 1
            except PermissionError as e:
                log_message("Permission Denied", recovery_file, current_file, str(e))
                files_protected_or_no_access += 1
            except OSError as e:
                log_message("Failed", recovery_file, current_file, str(e))
                files_failed_to_move += 1

    folder_counter += 1

    # Throttle the script by adding a short sleep after processing each folder
    time.sleep(throttle_duration)  # Adjust the sleep duration as needed

    # Update progress every 10 folders to reduce clutter
    if folder_counter % 10 == 0 or folder_counter == total_folders:
        print(f"Progress: {folder_counter}/{total_folders} folders ({(folder_counter / total_folders) * 100:.2f}%)")

# End timer
end_time = time.time()
elapsed_time = end_time - start_time

log_message("Summary", "", "", "Completed processing files.")
log_message("Summary", "", "", f"Total new directories created: {new_dirs_created}")
log_message("Summary", "", "", f"Total files failed to move: {files_failed_to_move}")
log_message("Summary", "", "", f"Total Directory protected/no access: {files_protected_or_no_access}")
log_message("Summary", "", "", f"Total time elapsed: {elapsed_time:.2f} seconds")
