from numpy import array
from numpy import tensordot
tensor1 = array([
  [[1,2,3],    [4,5,6],    [7,8,9]],
  [[13,12,13], [14,15,16], [17,18,19]],
  [[24,22,23], [24,25,26], [27,28,29]],
  ])
tensor2 = array([
  [[1,4,3],    [4,5,6],    [7,8,9]],
  [[11,13,13], [14,15,16], [17,18,19]],
  [[21,25,23], [24,26,26], [27,28,29]],
  ])

print("tensor1",tensor1)
print("tensor2",tensor2)
print("sum of tensors", "is")
sum = tensor1 + tensor2
print(sum)

print("difference of tensors",  "is")

diff = tensor1 - tensor2
print(diff)

print("product of tensors",  "is")

prod = tensor1 * tensor2
print(prod)

print("division of tensors",  "is")

division = tensor1 / tensor2
print(division)

print("dot product of tensors",  "is")

dotproduct = tensordot(tensor1, tensor2, axes=0)
print(dotproduct)
