import re


#1
s = str(input())

if re.search(r"ab*", s):
    print("Valid")
else:
    print("Invalid")


#2
txt = str(input())

if re.search(r"ab{2,3}", txt):
    print("Match")
else:
    print("No match")



#3
t = str(input())

if re.search(r"[a-z]+_[a-z]+", t):
    print("Match")
else:
    print("No match")



#4
string = str(input())

if re.search(r"[A-Z][a-z]+", string):
    print("Match")
else:
    print("No match")


#5
a = str(input())

if re.search(r"a.*b", a):
    print("Match")
else:
    print("No match")



#6
b = str(input())

x = re.sub(r"[ ,.]", ":", b)
print(x)



#7
c = str(input())

res = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), c)
print(res)



#8
d = str(input())

r = re.split(r"(?=[A-Z])", d)
print(r)




#9
e = str(input())

y = re.sub(r"([A-Z])", r" \1", e)
print(y.strip())



#10
f = str(input())

w = re.sub(r"([A-Z])", r"_\1", f).lower()
print(w.strip("_"))