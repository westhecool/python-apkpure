import os
import shutil
import sys
f = open("download-list.txt", "r")
for line in f.readlines():
    id = line.strip()
    if os.path.exists(f"./apks/{id}"):
        continue
    if os.system(f"{sys.executable} cli.py download {id} -d ./apks/{id}") != 0:
        print("Failed to download", id)
        try:
            shutil.rmtree(f"./apks/{id}")
        except:
            pass
f.close()