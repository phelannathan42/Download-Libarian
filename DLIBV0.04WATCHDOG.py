import os
import shutil
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Construct the path to the download folder
download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

class FileSorter(FileSystemEventHandler):
    def on_created(self, event):
        temp_file_paths = [
            os.path.join(download_folder, f)
            for f in os.listdir(download_folder)
            if f.endswith(('.tmp', '.crdownload'))
        ]

        # Wait until the temp files are no longer present
        while any(os.path.exists(p) for p in temp_file_paths):
            time.sleep(1)

        # Sort the files in the download folder
        files = [
            f
            for f in os.listdir(download_folder)
            if not f.endswith(('.tmp', '.crdownload')) and os.path.getsize(os.path.join(download_folder, f)) > 1_000
        ]
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            dest_folder = os.path.join(download_folder, file_ext[1:])
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            src_file = os.path.join(download_folder, file)
            dest_file = os.path.join(dest_folder, file)
            shutil.move(src_file, dest_file)

# Create the file system event handler
event_handler = FileSorter()

# Create the observer
observer = Observer()

# Set the observer to watch the download folder
observer.schedule(event_handler, download_folder, recursive=True)

# Start the observer
observer.start()

# Run the observer indefinitely
try:
    while True:
        # Sort the files every 10 seconds
        time.sleep(10)
        event_handler.on_created(None)
except KeyboardInterrupt:
    observer.stop()

# Join the observer thread
observer.join()
