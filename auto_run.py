import time
import os
import subprocess
import organize_downloads
from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, FileCreatedEvent, FileSystemEventHandler

home_dir = "C:\\Users\\Arun"
downloads_path = os.path.join(home_dir, "Downloads")

class Watcher():
    def __init__(self) -> None:
        self.observer = Observer()
        self.path = downloads_path

    def run(self):
        event_handler = MyHandler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(30)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Failed to start observer")

        self.observer.join()

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        file_limit = 1
        current_file_count = self.count_files()

        if current_file_count > file_limit:
            print("Downloads contains more than", file_limit, ", Organizing Downloads folder")
            subprocess.run(["python3", "organize_downloads.py"])
        

    def count_files(self) -> int:
        file_count = 0
        for entry in os.scandir(downloads_path):
            if entry.is_file():
                file_count += 1
        return file_count

#def main():

if __name__ == "__main__":
    w = Watcher()
    w.run()



