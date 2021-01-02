import sqlite3
import sys
import shutil
import random
import os 
from os import path as os_path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

path_root = "/Volumes/KOBOeReader/"
path_to_database = path_root + ".kobo/KoboReader.sqlite"
path_to_kobo = path_root

def get_shelves():
    conn= sqlite3.connect(path_to_database)
    c=conn.cursor()
    conn.text_factory=str
    c.execute("SELECT Name from SHELF ORDER BY NAME")
    shelves = [r[0] for r in c.fetchall()]
    conn.close()
    return shelves

def add_shelf(shelf_name=""):
    if shelf_name == "":
        shelf_name = input("New Shelf Name? ")
    if shelf_name in get_shelves():
        print("Shelf Name already exists")
        return False
    shelf_id = random.randint(0,10000000000000)
    conn= sqlite3.connect(path_to_database)
    c=conn.cursor()
    conn.text_factory=str
    c.execute("INSERT INTO SHELF VALUES(NULL,?,?,NULL,?,'UserTag', false, true, false, NULL, NULL )",(str(shelf_id), shelf_name, shelf_name))
    conn.commit()
    print("Added " + shelf_name)    
    conn.close()

def add_book():
    Tk().withdraw
    filename = askopenfilename()
    print(filename)

def add_all_papers():
    for path,subdirs, files in os.walk("./pdfs"):
        for file_name in files:
            print(path_root + file_name)
            if file_name[-4:] == ".pdf" and not os_path.exists(path_root+file_name):
                shelf_name = path.split("/")[-1]
                add_shelf(shelf_name)

                full_file_path = os.path.join(path, file_name)                
                newPath = shutil.copy(full_file_path, path_to_kobo)
                kobo_file_name = "file:///mnt/onboard/"+file_name

                conn = sqlite3.connect(path_to_database)
                c=conn.cursor()
                c.execute("INSERT INTO SHELFCONTENT VALUES(?,?, NULL, FALSE, FALSE)", (shelf_name,kobo_file_name))
                print("added " + file_name + " into " + shelf_name)
                conn.commit()
                conn.close()

if __name__ == "__main__":
    print("UwU welcome to the book adder!")
    while True:
        print("1. Print Shelves\n2. Add Shelves\n3. Add Books to Shelves\n4. Add All Papers\n5. Exit")
        command = input() 
        if command == "1":
            print(get_shelves())
        if command == "2":
            add_shelf()
        if command == "3":
            add_book()
        if command == "4":
            add_all_papers()
        if command == "5":
            break
    print("See you space cowboy")