import os
import shutil
import glob
home_dir = "C:\\Users\\Arun"
exclude_types = [".crdownload", ".html"]

def get_newest_downloaded_file(downloads_path) -> str:
        most_recent_file = ""
        most_recent_time = 0
        for file in os.scandir(downloads_path):
            if file.is_file():
                mod_time = file.stat().st_mtime_ns
                if mod_time > most_recent_time:
                    most_recent_file = file.name
                    most_recent_time = mod_time

        return most_recent_file

#check type of file
def get_extension_type(file) -> str:
    extension = os.path.splitext(file)
    root = extension[0]
    ext = extension[1]
    #print(root, ext)
    return ext

#make folders and categorize based on file type
#example: application into applications folder, pdf into pdf folder, mp3 into mp3 folder
#if folder exists, update folder, else create new folder
def create_folder(file, extension, downloads_path):
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

def move_to_folder(file_to_move, extension_type, downloads_path):
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

def main():
    # cwd = os.getcwd()
    # print("Current Directory: ", cwd)
    downloads_path = os.path.join(home_dir, "Downloads")
    #print(downloads_path)

    #file_types = [".exe", ".pdf", ".mp4", ".mp3", ".jpg", ".png", ".ydk", ".zip"]

    file_to_move = get_newest_downloaded_file(downloads_path)
    print(file_to_move, type(file_to_move))

    extension_type = get_extension_type(file_to_move)
    print(extension_type, type(extension_type))
        
    move_to_folder(file_to_move, extension_type, downloads_path)

if __name__ == "__main__":
    main()