from qutip import *
import numpy as nump
import matplotlib.pyplot as matplot
from math import *
import seaborn as seabrn



ket0 = basis(2,0).unit() 
ket1 = basis(2,1).unit() 
psip = (basis(2,0)+basis(2,1)*1j).unit() 
psim = (basis(2,0)-basis(2,1)*1j).unit() 

def GetCoin(coin_angle):
    C_hat = qutip.Qobj([[cos(radians(coin_angle)), sin(radians(coin_angle))],  
                     [sin(radians(coin_angle)), -cos(radians(coin_angle))]])
    return C_hat

def GetShift(t):
    sites = 2*t+1
    shift_l = qutip.Qobj(nump.roll(nump.eye(sites), 1, axis=0)) 
    shift_r = qutip.Qobj(nump.roll(nump.eye(sites), -1, axis=0)) 
    S_hat = tensor(ket0*ket0.dag(),shift_l) + tensor(ket1*ket1.dag(),shift_r) 
    return S_hat

def GetWalk(t,coin_angle):
    sites = 2*t+1
    C_hat = GetCoin(coin_angle) 
    S_hat = GetShift(t)     
    W_hat = S_hat*(tensor(C_hat,qeye(sites))) 
    return W_hat

def ApplyDephasing(t,qstate,p_c):
    sites=2*t+1
    dstate = (1-p_c)*qstate+p_c*(tensor(sigmaz(),qeye(sites))*qstate*tensor(sigmaz(),qeye(sites)))
    return dstate

def ApplyDepolarization(t,qstate,p_c):
    sites=2*t+1
    dstate = (1-p_c)*qstate+p_c/3*(tensor(sigmax(),qeye(sites))*(qstate)*tensor(sigmax(),qeye(sites))*
                           tensor(sigmay(),qeye(sites))*(qstate)*tensor(sigmay(),qeye(sites))*
                           tensor(sigmaz(),qeye(sites))*(qstate)*tensor(sigmaz(),qeye(sites)))
    return dstate



def GetQWalk_gen_markov(t,qubit_state,coin_angle,p_c):
    sites=2*t+1
    Position_state = basis(sites,t)           
    Psi = ket2dm(tensor(qubit_state,Position_state))   
    W_hat = GetWalk(t,coin_angle)                       
    for i in range(t):                               
        Psi = W_hat*ApplyDephasing(t,Psi,p_c)*W_hat.dag() 
    return Psi                                      

def GetMeasurement(t,Psi,z):
    sites=2*t+1
    prob=[]
    for i in range(0,sites,z):
        M_p = basis(sites,i)*basis(sites,i).dag()
        Measure = tensor(qeye(2),M_p)                  
        p = abs((Psi*Measure).tr())                   
        prob.append(p)
    return prob


def GetPlotParticlePos(P_p):
    lattice_positions = range(-len(P_p)+1,len(P_p)+1,2)
    matplot.plot(lattice_positions,P_p)
    matplot.xlim([-len(P_p)+1,len(P_p)+1])           
    matplot.ylim([min(P_p),max(P_p)+0.01])
    matplot.ylabel(r'$Probablity Distribution$')
    matplot.xlabel(r'$Particle \ position$')
    matplot.show()


Psi_t = GetQWalk_gen_markov(150,psip,65,0.01) 
P_p  = GetMeasurement(150,Psi_t,2)             
GetPlotParticlePos(P_p)