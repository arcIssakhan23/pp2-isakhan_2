5
#1
print("==================================================================")
N = int(input())
square = (x*x for x in range(1, N+1))
for i in square:
    print(i)


#2
print("==================================================================")
def f(n):
    i = 0
    while i <= n:
        yield str(i)
        i += 2



n = int(input())
print(",".join(f(n)))
print("==================================================================")


#3

import sys

def f(m):
    
    i = 0
    while(i <= m):
        yield str(i) + " "
        i += 12

m = int(input())
for j in f(m):
    sys.stdout.write(j)

sys.stdout.write("\n")

#4
print("==================================================================")

a = list(map(int, input().split()))

def square_generator(start, end):
    for x in range(start, end + 1):
        yield x * x

b = a[0]
k = a[1]

s = square_generator(b, k)
for i in s:
    print(i)

print("==================================================================")


#5
def fun(y):
    cnt = y
    while cnt > 0:
        yield cnt
        cnt -= 1


y = int(input())
ctr = fun(y)
for j in ctr:
    print(j)


print("==================================================================")
