# Recovery File Mover Script

## Description

This Python script facilitates the movement and synchronization of files from a recovery directory to a current directory, ensuring that only the newest versions of files are retained. It handles permission issues gracefully, logs all actions in a CSV file, and supports long file paths.

## Features

- **Directory Structure Maintenance**: Ensures the directory structure in the current directory matches the recovery directory.
- **File Comparison**: Compares modification times to decide whether to move a file from the recovery directory to the current directory.
- **Detailed Logging**: Logs all actions (e.g., moves, skips, errors) in a CSV file stored on the desktop.
- **Error Handling**: Manages permission errors and inaccessible files, logging these issues for review.
- **Progress Tracking**: Provides a progress update in the terminal for every 10 folders processed.
- **Performance Management**: Allows for throttling with adjustable sleep duration between folder processing.

## Usage

1. **Set Up Directories**: Define the `base_recovery_dir` and `current_dir` variables to point to your recovery and current directories, respectively.
2. **Run the Script**: Execute the script to start the file moving and synchronization process.
3. **Review Logs**: Check the generated CSV log file on your desktop for a detailed summary of all actions and any issues encountered.

## Requirements

- Python 3.x
- Standard Python libraries: `os`, `shutil`, `csv`, `datetime`, `time`

## Example

```python
# Define the root directories
base_recovery_dir = r"J:\SR116711"
current_dir = r"*****************"

# Run the script
python move_recovery_files.py
