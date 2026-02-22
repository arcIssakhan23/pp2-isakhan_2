import math

#1
print("==================================================================")
d = float(input("Input degree: "))
rad = d * (math.pi / 180)
print("Output radian:", rad)

#2
print("==================================================================")
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
area_trapezoid = (b1 + b2) * h / 2
print("Expected Output:", area_trapezoid)

#3
print("==================================================================")
s = int(input("Input number of sides: "))
l = float(input("Input the length of a side: "))
area_polygon = (s * l**2) / (4 * math.tan(math.pi / s))
print("The area of the polygon is:", round(area_polygon))

#4
print("==================================================================")
base = float(input("Length of base: "))
h_para = float(input("Height of parallelogram: "))
area_parallelogram = base * h_para
print("Expected Output:", area_parallelogram)
print("==================================================================")