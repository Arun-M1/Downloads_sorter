from pathlib import Path
import time
import shutil

#create testing directory and files
def create_test_files():
    test_dir = Path.home().joinpath("Downloads_Test")
    test_dir.mkdir(exist_ok=True)

    print(f"Creating test file in test directory {test_dir}\n")

    test_files = [
        "sample.pdf",
        "sample.mp3",
        "sample.jpg",
        "sample.mp4",
        "sample.zip",
        "sample.py",
    ]

    for file_name in test_files:
        file_path = test_dir.joinpath(file_name)
        file_path.touch()
        print(f"Created {file_name}")
        time.sleep(0.5)
    
    print(f"Test files created.")

#delete testing directory
def cleanup_test_dir():
    test_dir = Path.home().joinpath("Downloads_Test")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print(f"Removed testing directory {test_dir}")
    else:
        print(f"testing directory does not exist.")


if __name__ == "__main__":
    create_test_files()
    #cleanup_test_dir()