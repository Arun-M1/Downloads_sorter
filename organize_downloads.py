import os
import shutil
import glob
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

exclude_types = [".crdownload", ".html", ".tmp", ".part"]

class DownloadsOrganizer(FileSystemEventHandler):
    def __init__(self, downloads_path):
        self.downloads_path = Path(downloads_path)

    def on_created(self, event):
        # return super().on_created(event)
        #write own logic here
        if event.is_directory:
            print(f"Error: current {event} is a directory, not a file!")
            return

        file_path = Path(event.src_path)
        extension_type = self.get_extension_type(file_path)
        print(f"file path: {file_path}, extension type of file: {extension_type}")
        # self.create_folder(event, extension_type, self.downloads_path)
        # self.move_to_folder(event, extension_type, self.downloads_path)

    #check type of file
    def get_extension_type(self, file_path) -> str:
        extension = os.path.splitext(str(file_path))
        root = extension[0]
        ext = extension[1]
        print(root, ext)
        return ext

    #make folders and categorize based on file type
    #example: application into applications folder, pdf into pdf folder, mp3 into mp3 folder
    #if folder exists, update folder, else create new folder
    def create_folder(self, file, extension, downloads_path):
        new_folder = os.path.join(downloads_path, extension)
        try:
            os.makedirs(new_folder)
            print(f"Successfully created the folder: '{new_folder}'")
        except FileExistsError:
            print(f"The file `{new_folder}` already exists.")
        except Exception as e:
            print(f"Error occurred: {e}")

    # def update_folder(file, target_folder):
    #     try:
    #         shutil.move(os.path.join(downloads_path, file), target_folder))
    #         print(f"Moved file '{os.path.join(downloads_path, file_to_move)} into '{target_folder}'")
    #     except Exception as e:
    #         print(f"Error occurred: {e}")

    def move_to_folder(self, file_to_move, extension_type, downloads_path):
            #check if folder is subfolder of downloads
            if extension_type not in exclude_types:
                folder_name = os.path.join(downloads_path, extension_type)
                if not os.path.isdir(folder_name):
                    #create if not
                    print(f"attemping to create folder '{folder_name}")
                    create_folder(file_to_move, extension_type, downloads_path)
                #add if so
                else:
                    print("folder already exists")

                try:
                    shutil.move(os.path.join(downloads_path, file_to_move), folder_name)
                    #check if file already exists with name, if so, delete old copy of file and move new one
                    print(f"Moved file '{os.path.join(downloads_path, file_to_move)} into '{folder_name}'")
                except Exception as e:
                    print(f"Error occurred: {e}")

def main(custom_path=None):
    if custom_path:
        downloads_path = Path(custom_path)
    else:
        downloads_path = Path.home().joinpath("Downloads") #works for windows, mac, linux
    
    #print(downloads_path)
    if not downloads_path.exists():
        print(f"Error: Downloads folder was not found at {downloads_path}")
        return

    #file_types = [".exe", ".pdf", ".mp4", ".mp3", ".jpg", ".png", ".ydk", ".zip"]
    print(f"Program running continuously in {downloads_path}")
    print(f"Press ctrl c to stop\n")

    organizer_obj = DownloadsOrganizer(downloads_path)

    observer_obj = Observer()
    observer_obj.schedule(organizer_obj, str(downloads_path), recursive=False)
    observer_obj.start()

    print("Waiting for new downloads\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer_obj.stop()
        print(f"Stopped waiting")
    
    observer_obj.join()

if __name__ == "__main__":
    test_dir = Path.home().joinpath("Downloads_Test")
    
    if test_dir.exists():
        main(test_dir)
    else:
        main()