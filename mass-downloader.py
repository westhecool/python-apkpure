import os
import sys
f = open("download-list.txt", "r")
for line in f.readlines():
    id = line.strip()
    if os.path.exists(f"./apks/{id}"):
        continue
    os.system(f"{sys.executable} cli.py download {id} -d ./apks/{id}")
f.close()