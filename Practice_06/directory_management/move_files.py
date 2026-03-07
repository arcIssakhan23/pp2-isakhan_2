from pathlib import Path
import shutil

source = Path("just_file/another_one")

copy_folder = Path("copied_files")
move_folder = Path("moved_files")

copy_folder.mkdir(exist_ok=True)
move_folder.mkdir(exist_ok=True)

for file in source.glob("*.txt"):

    shutil.copy(file, copy_folder / file.name)

    shutil.move(file, move_folder / file.name)

print("Files copied and moved")