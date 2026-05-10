import os

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")

        if os.path.exists(self.filename):
            print("File found.")
            return True

        print("File not found.")
        return False

    def create_output_folder(self):
        if not os.path.exists("output"):
            os.mkdir("output")