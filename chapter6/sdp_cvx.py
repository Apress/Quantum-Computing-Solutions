
import cvxpy as cvxp
import numpy as nump

n = 3
p = 3
nump.random.seed(1)
CMat = nump.random.randn(n, n)
AMat = []
bMat = []
for i in range(p):
    AMat.append(nump.random.randn(n, n))
    bMat.append(nump.random.randn())

XMat = cvxp.Variable((n,n), symmetric=True)

constraints = [XMat >> 0]
constraints += [
    cvxp.trace(AMat[i]@XMat) == bMat[i] for i in range(p)
]
problem = cvxp.Problem(cvxp.Minimize(cvxp.trace(CMat@XMat)),
                  constraints)
problem.solve()


print("The optimal value of the problem is", problem.value)
print("A solution X is")
print(XMat.value)