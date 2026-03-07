names = ["Tom", "Anna", "Bob"]
scores = [90, 85, 88]

for i, name in enumerate(names):
    print(i, name)

print("========================================================")

for name, score in zip(names, scores):
    print(name, score)