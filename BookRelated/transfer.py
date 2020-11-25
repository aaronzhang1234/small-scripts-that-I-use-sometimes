import sqlite3
import sys
import shutil
import os 
from os import path as os_path
path_root = "/Volumes/KOBOeReader/"

if __name__ == "__main__":
    path_to_database = path_root + ".kobo/KoboReader.sqlite"
    path_to_kobo = path_root

    for path,subdirs, files in os.walk("./pdfs"):
        for file_name in files:
            print(path_root + file_name)
            if file_name[-4:] == ".pdf" and not os_path.exists(path_root+file_name):
                full_file_path = os.path.join(path, file_name)
                print(full_file_path)
                
                newPath = shutil.copy(full_file_path, path_to_kobo)

                kobo_file_name = "file:///mnt/onboard/"+file_name
                conn = sqlite3.connect(path_to_database)
                print(kobo_file_name)

                c=conn.cursor()

                c.execute("INSERT INTO SHELFCONTENT VALUES('papers',?, NULL, FALSE, FALSE)", (kobo_file_name,))

                conn.commit()

                conn.close()