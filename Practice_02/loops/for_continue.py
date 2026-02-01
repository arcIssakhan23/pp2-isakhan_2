#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)


#2
a = [1, 2, 7, 3, 4, 5]
for i in a:
    if i == 7:
        continue
    print(i)


#3
b = [1, 2, "7", 3, 4, 5]
for i in b:
    if i == "7":
        continue
    print(i)



#4
c = [1, False, "banana", '3', True, "5", 7.0009]
for i in c:
    if i == True:
        continue
    print(i)



#5
d = [1, 2, 7, 3, 4, 5]
for i in range(0, 6):
    if i == 7:
        continue
    print(i)