import sqlite3
import sys
import shutil

if __name__ == "__main__":
    #path_to_database = "./KoboReader.sqlite"
    path_to_database = "/Volumes/KOBOeReader/.kobo/KoboReader.sqlite"
    path_to_kobo = "/Volumes/KOBOeReader"
    file_to_upload = str(sys.argv[1])

    newPath = shutil.copy(file_to_upload, path_to_kobo)


    kobo_file_name = "file:///mnt/onboard/"+file_to_upload
    conn = sqlite3.connect(path_to_database)
    print(kobo_file_name)

    c=conn.cursor()

    c.execute("INSERT INTO SHELFCONTENT VALUES('papers',?, NULL, FALSE, FALSE)", (kobo_file_name,))

    conn.commit()

    conn.close()