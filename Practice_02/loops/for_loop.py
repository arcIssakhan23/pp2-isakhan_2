#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)


#2
for i in "banana":
    print(i)


#3
for j in range(6):
    print(j)
else:
    print("Finally finished!")


#4
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
    for y in fruits:
        print(x, y)


#5
for k in range(0, 100):
    if k == 10:
        break
    print(k**k)