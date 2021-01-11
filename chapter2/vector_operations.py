from numpy import array

vector1 = array([1, 2, 3])

vector2 = array([2, 3, 4])
print("dot product of", vector1,", ",vector2,"is")
product = vector1.dot(vector2)
print(product)

scalarval = 0.3
scalarprod = scalarval*vector1
print("scalar multiplied",scalarval,",",vector1,"is")
print(scalarprod)


print("sum of", vector1,", ",vector2,"is")
sum = vector1 + vector2
print(sum)

print("difference of", vector1,", ",vector2,"is")
diff = vector1 - vector2
print(diff)

print("product of", vector1,", ",vector2,"is")
prod = vector1 * vector2
print(prod)

print("divison of", vector1,", ",vector2,"is")
dividedby = vector1 / vector2
print(dividedby)
