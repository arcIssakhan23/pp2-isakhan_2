from functools import reduce

numbers = [1, 2, 3, 4, 5]

sq = list(map(lambda x: x*x, numbers))
print("Squared:", sq)

even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

_sum = reduce(lambda a, b: a + b, numbers)
print("Sum:", _sum)