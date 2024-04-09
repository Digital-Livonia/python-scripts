#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script to convert file structure into SQL statemens for Directus.
# Script is NOT generic, it is for a certain folder structure.


"""File renamer"""

import sys
import os
import os.path
from PIL import Image
import uuid
import datetime

os.system('clear')

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# in python 3
#dirName = input("Kaust kus asuvad failid: ")

# see peaks ainult maci puhul olema aktiivne
# dirName = (dirName.replace("\\", "")).rstrip()

dirName = "/Volumes/AV-SSD1/TLU/pitserid"
dirNameFile = "/Volumes/AV-SSD1/TLU"
fileSave = "directus_pitserid_files.sql"

if dirName=="":
    input("\n\nKausta nimi puudu!")
    sys.exit()

dirContent = os.listdir(dirName)

i=0

# if previous file exists, lets add date and time to it
if os.path.exists(dirNameFile + '/' + fileSave):
    x = datetime.datetime.now()
    #os.rename(dirNameFile + '/' + fileSave, dirNameFile + '/prev_' + x.strftime("%f") + '_' + fileSave)

with open(dirNameFile + '/' + fileSave, 'w') as f:    
    for dirContentList in dirContent:
        dir2Content = os.listdir(dirName + '/' + dirContentList)
        for dir2ContentList in dir2Content:
            dir3Content = os.listdir(dirName + '/' + dirContentList + '/' + dir2ContentList)
            for dir3ContentList in dir3Content:
                dir4Content = os.listdir(dirName + '/' + dirContentList + '/' + dir2ContentList + '/' + dir3ContentList )
                for fileName in dir4Content:
                    fileNameArr = fileName.split(".")
                    fileExt = fileNameArr[len(fileNameArr)-1]
                    fileBase = fileNameArr[0]
                    file_path = dirName + '/' + dirContentList + '/' + dir2ContentList + '/' + dir3ContentList + '/'
                    file_size = os.path.getsize(file_path + fileName)
                    img = Image.open(file_path + fileName)
                    width = img.width
                    height = img.height
                    uuid4 = uuid.uuid4()
                    os.rename(file_path + fileName, file_path + str(uuid4) + '.' + fileExt)
                    f.write ("INSERT INTO directus.directus_files VALUES('"+str(uuid4)+"', 'local', '"+str(uuid4)+'.'+ fileExt +"','" + fileName + "', '" + fileBase +"','image/" + fileExt +"', '93b1a870-cb8a-4ad5-b09d-4ef7cad4c5de', 'e3bbad11-0ce4-455d-9fab-ef67ce0bb910','2022-09-21 16:00', NULL,NULL,NULL, "+str(file_size)+", "+str(width)+", "+str(height)+", NULL, NULL, 'pitserid"+ '/' + dirContentList + '/' + dir2ContentList + '/' + dir3ContentList+"', NULL, NULL, NULL);\n")
