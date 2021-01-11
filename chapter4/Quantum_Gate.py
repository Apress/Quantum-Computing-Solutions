import numpy as nump
from itertools import product

class Quantum_Gate:
    def __init__(self, matrix):
        self._data = nump.array(matrix, dtype=nump.complex64)

        assert len(self._data.shape) == 2
        assert self._data.shape[0] == self._data.shape[1]

        self._n = nump.log2(self._data.shape[0])

        assert self._n.is_integer()

        self._n = int(self._n)

    def __matmul__(self, other):
        return Quantum_Gate(nump.kron(self._data, other._data))

    def __pow__(self, n, modulo=None):
        x = self._data.copy()

        for _ in range(n - 1):
            x = nump.kron(x, self._data)

        return Quantum_Gate(x)


I_Gate = Quantum_Gate([[1, 0], [0, 1]])
H_Gate = Quantum_Gate(nump.array([[1, 1], [1, -1]]) / nump.sqrt(2))
X_Gate = Quantum_Gate([[0, 1], [1, 0]])
Y_Gate = Quantum_Gate([[0, -1j], [1j, 0]])
Z_Gate = Quantum_Gate([[1, 0], [0, -1]])


def U_Quantum_Gate(f, n):
    m = n + 1

    U = nump.zeros((2**m, 2**m), dtype=nump.complex64)

    def bin2int(xs):
        r = 0
        for i, x in enumerate(reversed(xs)):
            r += x * 2 ** i
        return r

    for xs in product({0, 1}, repeat=m):
        x = xs[:~0]
        y = xs[~0]

        z = y ^ f(*x)

        instate = bin2int(xs)
        outstate = bin2int(list(x) + [z])
        U[instate, outstate] = 1

    return Quantum_Gate(U)
