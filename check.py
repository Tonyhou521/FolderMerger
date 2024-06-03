import os
import csv

# Define the root directory and log file
root_dir = r"J:\SR116711"  # Change to your desired directory
log_file = r"C:\Users\SHENGTAOHOU\Desktop\long_path_files_log.csv"

# Initialize the log file and write the CSV header
with open(log_file, 'w', newline='', encoding='utf-8') as log:
    csv_writer = csv.writer(log)
    csv_writer.writerow(["File Path", "Path Length"])

# Function to log messages in CSV format
def log_message(path, length):
    with open(log_file, 'a', newline='', encoding='utf-8') as log:
        csv_writer = csv.writer(log)
        csv_writer.writerow([path, length])
    print(f"Logged: {path} | Length: {length}")

# Initialize counter
long_path_count = 0
max_path_length = 0
longest_path = ""

# Traverse the directory
for root, dirs, files in os.walk(root_dir):
    for name in files:
        file_path = os.path.join(root, name)
        path_length = len(file_path)
        
        if path_length > 260:
            long_path_count += 1
        
        if path_length > max_path_length:
            max_path_length = path_length
            longest_path = file_path
        
        log_message(file_path, path_length)

# Log the summary
with open(log_file, 'a', newline='', encoding='utf-8') as log:
    csv_writer = csv.writer(log)
    csv_writer.writerow([])
    csv_writer.writerow(["Summary"])
    csv_writer.writerow(["Total files with paths longer than 260 characters:", long_path_count])
    csv_writer.writerow(["Longest path length:", max_path_length])
    csv_writer.writerow(["Longest path:", longest_path])

print(f"Total files with paths longer than 260 characters: {long_path_count}")
print(f"Longest path length: {max_path_length}")
print(f"Longest path: {longest_path}")
print("Scanning completed.")
