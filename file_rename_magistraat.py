import os
import uuid
from PIL import Image
import mimetypes

# Base directory containing directories to process
dirName = "/Users/hembo/Library/CloudStorage/GoogleDrive-hembo@tlu.ee/Shared drives/Digital Livonia/Andmed mujalt/Rahvusarhiiv/Magistraat/lisatud_nov_2023"
# Directory to save the output file
dirNameFile = dirName
# Output file name
fileSave = "directus_magistraat_files.sql"

directusFolderID = "0fa90820-4709-4b25-88d4-a4cff60e6e1b"
directusUserID = "e3bbad11-0ce4-455d-9fab-ef67ce0bb910"
directusFileUploadDate = "2024-02-09 10:00"

with open(os.path.join(dirNameFile, fileSave), 'w') as f:
    dirContent = os.listdir(dirName)
    for dirContentList in dirContent:
        full_dir_path = os.path.join(dirName, dirContentList)
        if not dirContentList.startswith('.') and os.path.isdir(full_dir_path):
            dir2Content = os.listdir(full_dir_path)
            for fileName in dir2Content:
                if not fileName.startswith('.'):
                    full_file_path = os.path.join(full_dir_path, fileName)
                    # Process only if it's a file
                    if os.path.isfile(full_file_path):
                        fileNameArr = fileName.split(".")
                        fileExt = fileNameArr[-1]  # Simpler way to get the last item
                        fileBase = fileNameArr[0]
                        file_size = os.path.getsize(full_file_path)
                        fileMime = mimetypes.MimeTypes().guess_type(full_file_path)[0]  # Update this line to use mimetypes
                        img = Image.open(full_file_path)
                        width, height = img.size
                        uuid4 = uuid.uuid4()

                        # Rename image files
                        new_file_name = f"{uuid4}.{fileExt}"
                        new_file_path = os.path.join(full_dir_path, new_file_name)
                        os.rename(full_file_path, new_file_path)

                        # Write SQL into output file
                        f.write(f"INSERT INTO directus.directus_files VALUES('{uuid4}', 'local', '{new_file_name}', '{fileName}', '{fileBase}', '{fileMime}', '{directusFolderID}', '{directusUserID}', '{directusFileUploadDate}', NULL, NULL, NULL, {file_size}, {width}, {height}, NULL, NULL, '{dirContentList}', NULL, NULL, NULL, NULL, NULL);\n")

