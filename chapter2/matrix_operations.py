import numpy

mat1 = numpy.array([[1, 3], [4, 6]])
mat2 = numpy.array([[7, 9], [11, 15]])
print ("Addition of  matrices ", mat1,",", mat2,"is")
print (numpy.add(mat1,mat2))


print ("Subtraction of  matrices ", mat1,",", mat2,"is")
print (numpy.subtract(mat1,mat2))

print ("Product of  matrices ", mat1,",", mat2,"is")
print (numpy.multiply(mat1,mat2))

print ("Dot Product of  matrices ", mat1,",", mat2,"is")
print (numpy.dot(mat1,mat2))

print ("Division of  matrices ", mat1,",", mat2,"is")
print (numpy.divide(mat1,mat2))

print ("Transpose of ", mat1,"is")
print (mat1.T)
