
import cvxpy as cp
import numpy as np

m = 20
n = 15
np.random.seed(1)
A = np.random.randn(m, n)
print(A)
b = np.random.randn(m)
print(b)

x = cp.Variable(n)
print(x)
cost = cp.sum_squares(A*x - b)
prob = cp.Problem(cp.Minimize(cost))
prob.solve()

print("\nThe optimal value is", prob.value)
print("The optimal x is")
print(x.value)
print("The norm of the residual is ", cp.norm(A*x - b, p=2).value)