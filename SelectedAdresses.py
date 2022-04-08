import os
import shutil
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
print("select File:")
filename_Filelist = filedialog.askopenfilename()
root.withdraw

adress_file = open(filename_Filelist, "r")
address_list = adress_file.read().splitlines()

for adress in address_list:
    filenames = adress.split(";")
    os.rename(filenames[0], filenames[1])