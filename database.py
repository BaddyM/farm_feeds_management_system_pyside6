import sys
import os

class Database:
    def __init__(self):
        # Create sqlite connection
        global file_path
        self.db_path = ""
        try:
            if sys.platform == "windows":
                file_path = "C:/farm_system_db/data"
            elif sys.platform == "linux":
                file_path = "files/data"
            os.makedirs(file_path, 754)
        except:
            pass

        # create the file
        if sys.platform == "windows":
            self.db_path = "C:/farm_system_db/data/database.db"
        elif sys.platform == "linux":
            self.db_path = "files/data/database.db"

        try:
            open(self.db_path, "a+")
        except:
            pass