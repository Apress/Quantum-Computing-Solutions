import numpy as nump
from grove.pyqaoa.maxcut_qaoa import maxcut_qaoa
import pyquil.api as pyquilapi
qvm_session = pyquilapi.QVMConnection()

configuration_ring = [(0,1),(1,2),(2,3),(3,0)]

steps = 2
inst = maxcut_qaoa(graph=configuration_ring, steps=steps)
betas, gammas = inst.get_angles()
t = nump.hstack((betas, gammas))
param_program = inst.get_parameterized_program()
program = param_program(t)
wave_function = qvm_session.wavefunction(program)
wave_function = wave_function.amplitudes

for state_index in range(inst.nstates):
    print(inst.states[state_index], nump.conj(wave_function[state_index])*wave_function[state_index])