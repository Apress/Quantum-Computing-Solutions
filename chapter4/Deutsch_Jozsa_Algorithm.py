from Quantum_Register import Quantum_Register
from Quantum_Gate import H_Gate, I_Gate, U_Gate


def Check_If_Constant(g, n):
    qr = Quantum_Register(n + 1, '0' * n + '1')
    qr.Apply_Gate(H_Gate ** (n + 1))
    qr.Apply_Gate(U_Gate(g, n))
    qr.Apply_Gate(H_Gate ** n @ I_Gate)

    return qr.Get_Measure()[:~0] == '0' * n


def g1_func(v):
    return v


def g2_func(w):
    return 1


def g3_func(v, w):
    return v ^ w


def g4_func(v, w,x):
    return 0


print('g(v) = v is {}'.format('constant function' if Check_If_Constant(g1_func, 1) else 'balanced function'))
print('g(v) = 1 is {}'.format('constant function' if Check_If_Constant(g2_func, 1) else 'balanced function'))
print('g(v, w) = v ^ w is {}'.format('constant function' if Check_If_Constant(g3_func, 2) else 'balanced function'))
print('g(v, w, x) = 0 is {}'.format('constant function' if Check_If_Constant(g4_func, 3) else 'balanced function'))
