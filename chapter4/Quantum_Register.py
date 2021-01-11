import numpy as nump
from itertools import product
from Quantum_Gate import Quantum_Gate


class Quantum_Register:
    def __init__(self, n_qbits, init):
        self._n = n_qbits
        assert len(init) == self._n

        self._data = nump.zeros((2 ** self._n), dtype=nump.complex64)
        self._data[int('0b' + init, 2)] = 1

    def Get_Measure(self):
        probs = nump.real(self._data) ** 2 + nump.imag(self._data) ** 2
        states = nump.arange(2 ** self._n)
        mstate = nump.random.choice(states, size=1, p=probs)[0]
        return f'{mstate:>0{self._n}b}'

    def Apply_Gate(self, gate):
        assert isinstance(gate, Quantum_Gate)
        assert self._n == gate._n
        self._data = gate._data @ self._data
