import os
import shutil
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Construct the path to the download folder
download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

class FileSorter(FileSystemEventHandler):
    def on_created(self, event):
        # Sort the files in the download folder
        files = os.listdir(download_folder)
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
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

# Join the observer thread
observer.join()
