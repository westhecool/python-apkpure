import os
import shutil
import sys
list = open("download-list.txt", "r")
failed = open("failed.txt", "w")
for line in list.readlines():
    id = line.strip()
    if os.path.exists(f"./apks/{id}"):
        continue
    if os.system(f"{sys.executable} cli.py download {id} -d ./apks/{id}") != 0:
        print("Failed to download", id)
        failed.write(id + "\n")
        try:
            shutil.rmtree(f"./apks/{id}")
        except:
            pass
list.close()
failed.close()