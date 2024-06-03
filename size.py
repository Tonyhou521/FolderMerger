import os
import csv

def get_folder_sizes(path):
    folder_sizes = {}
    entries = [entry for entry in os.scandir(path) if entry.is_dir()]
    total_entries = len(entries)

    for i, entry in enumerate(entries):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(entry.path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if len(fp) >= 260:
                    fp = f"\\\\?\\{fp}"
                try:
                    total_size += os.path.getsize(fp)
                except OSError as e:
                    print(f"Error accessing file {fp}: {e}")
        folder_sizes[entry.name] = total_size
        
        # Simple progress display
        print(f"Processed {i + 1}/{total_entries} folders")
    
    return folder_sizes

def write_sizes_to_csv(folder_sizes, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Folder Name", "Size (GB)"])
        for folder, size in folder_sizes.items():
            writer.writerow([folder, size / (1024 ** 3)])

# Replace 'J:\\' with your network drive path
network_drive_path = '\\\\?\\J:\\'
csv_file_path = 'C:\\Users\\shengtaohou\\Desktop\\RecoveryLog\\Jsize.csv'
folder_sizes = get_folder_sizes(network_drive_path)
write_sizes_to_csv(folder_sizes, csv_file_path)

print(f"Folder sizes have been written to {csv_file_path}")
