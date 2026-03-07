import shutil
import os
#1 create file
with open("myfile.txt", 'w') as f:
    f.write("Sample text file was added!")

with open("myfile.txt") as f:
    print(f.read())

#2 copying file 

shutil.copy("myfile.txt", "newmyfile.txt")

with open("newmyfile.txt") as f:
    print(f.read())


#3 deleting 
os.remove("newmyfile.txt")


