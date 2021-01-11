import numpy as nump
from scipy import linalg as lina
from scipy.linalg import lstsq


def get_least_squares_fit(data, basis_matrix, weights=None, PSD=False, trace=None):
   
    c_mat = basis_matrix
    d_mat = nump.array(data)


    if weights is not None:
        w = nump.array(weights)
        c_mat = w[:, None] * c_mat
        d_mat = w * d_mat

    rho_fit_mat, _, _, _ = lstsq(c_mat.T, d_mat)
    
    print(rho_fit_mat)

    size = len(rho_fit_mat)
    dim = int(nump.sqrt(size))
    if dim * dim != size:
        raise ValueError("fitted vector needs to be a sqaure matrix")
    rho_fit_mat = rho_fit_mat.reshape(dim, dim, order='F')

    if PSD is True:
        rho_fit_mat = convert_positive_semidefinite_matrix#(rho_fit)

    if trace is not None:
        rho_fit_mat *= trace / nump.trace(rho_fit_mat)
    return rho_fit_mat



def convert_positive_semidefinite_matrix(mat, epsilon=0):
   

    if epsilon < 0:
        raise ValueError('epsilon nees to be positive ')

   
    dim = len(mat)
    v, w = lina.eigh(mat)
    for j in range(dim):
        if v[j] < epsilon:
            tmp = v[j]
            v[j] = 0.
            x = 0.
            for k in range(j + 1, dim):
                x += tmp / (dim - (j + 1))
                v[k] = v[k] + tmp / (dim - (j + 1))

    matrix_psd = nump.zeros([dim, dim], dtype=complex)
    for j in range(dim):
        matrix_psd += v[j] * nump.outer(w[:, j], nump.conj(w[:, j]))

    return matrix_psd


data = [12, 21, 23.5, 24.5, 25, 33, 23, 15.5, 28,19]
u_matrix = nump.arange(0, 10)

basis_matrix = nump.array([u_matrix, nump.ones(10)])



rho_fit_val = get_least_squares_fit(data,basis_matrix)


