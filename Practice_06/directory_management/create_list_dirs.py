from pathlib import Path

b = Path("just_file/another_one")
b.mkdir(parents=True, exist_ok=True)

files = ["a.txt", "b.txt", "c.txt"]

for n in files:
    f_p = b / n
    f_p.write_text("example text")


for item in Path(".").iterdir():
    print(item)

for file in Path("just_file").rglob("*.txt"):
    print(file)