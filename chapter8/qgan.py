
import pennylane as qganPenny
from pennylane import numpy as numcal
from pennylane.optimize import GradientDescentOptimizer as GDO

device = qganPenny.device('default.qubit', wires=3)


def GetQGANReal(phi, theta, omega):
    qganPenny.Rot(phi, theta, omega, wires=0)


def GetQGANGenerator(wireArray):
    qganPenny.RX(wireArray[0], wires=0)
    qganPenny.RX(wireArray[1], wires=1)
    qganPenny.RY(wireArray[2], wires=0)
    qganPenny.RY(wireArray[3], wires=1)
    qganPenny.RZ(wireArray[4], wires=0)
    qganPenny.RZ(wireArray[5], wires=1)
    qganPenny.CNOT(wires=[0,1])
    qganPenny.RX(wireArray[6], wires=0)
    qganPenny.RY(wireArray[7], wires=0)
    qganPenny.RZ(wireArray[8], wires=0)


def GetQGANDiscriminator(wireArray):
    qganPenny.RX(wireArray[0], wires=0)
    qganPenny.RX(wireArray[1], wires=2)
    qganPenny.RY(wireArray[2], wires=0)
    qganPenny.RY(wireArray[3], wires=2)
    qganPenny.RZ(wireArray[4], wires=0)
    qganPenny.RZ(wireArray[5], wires=2)
    qganPenny.CNOT(wires=[1,2])
    qganPenny.RX(wireArray[6], wires=2)
    qganPenny.RY(wireArray[7], wires=2)
    qganPenny.RZ(wireArray[8], wires=2)


@qganPenny.qnode(device)
def GetQGANRealDiscCircuit(phi, theta, omega, discWeights):
    GetQGANReal(phi, theta, omega)
    GetQGANDiscriminator(discWeights)
    return qganPenny.expval.PauliZ(2)


@qganPenny.qnode(device)
def GetQGANDiscCircuit(genWeights, discWeights):
    GetQGANGenerator(genWeights)
    GetQGANDiscriminator(discWeights)
    return qganPenny.expval.PauliZ(2)


def GetQGANRealTrue(discWeights):
    trueDiscriminatorOutput = GetQGANRealDiscCircuit(phi, theta, omega, discWeights)
    probabilityRealTrue = (trueDiscriminatorOutput + 1) / 2
    return probabilityRealTrue


def GetQGANFakeTrue(genWeights, discWeights):
    fakeDiscriminatorOutput = GetQGANDiscCircuit(genWeights, discWeights)
    probabilityFakeTrue = (fakeDiscriminatorOutput + 1) / 2
    return probabilityFakeTrue 


def GetQGANDiscriminatorCost(discWeights):
    cost = GetQGANFakeTrue(genWeights, discWeights) - GetQGANRealTrue(discWeights) 
    return cost


def GetQGANGeneratorCost(genWeights):
    return -GetQGANFakeTrue(genWeights, discWeights)


phi = numcal.pi / 6
theta = numcal.pi / 2
omega = numcal.pi / 7

numcal.random.seed(0)
epsValue = 1e-2
genWeights = numcal.array([numcal.pi] + [0] * 8) + numcal.random.normal(scale=epsValue, size=[9])
discWeights = numcal.random.normal(size=[9])

gdo = GDO(0.1)

print("Training the discriminator ")
for iteration in range(50):
    discriminator_weights = gdo.step(GetQGANDiscriminatorCost, discWeights) 
    discriminator_cost = GetQGANDiscriminatorCost(discriminator_weights)
    if iteration % 5 == 0:
        print("Iteration num {}: discriminator cost is = {}".format(iteration+1, discriminator_cost))

print(" discriminator - real true: ", GetQGANRealTrue(discWeights))
print("discriminator - fake true: ", GetQGANFakeTrue(genWeights, discWeights))

print("Training the generator.")


for iteration in range(200):
    generator_weights = gdo.step(GetQGANGeneratorCost, genWeights)
    generator_cost = -GetQGANGeneratorCost(generator_weights)
    if iteration % 5 == 0:
        print("Iteration num {}: generator cost is = {}".format(iteration, generator_cost))

print("discriminator - real true: ", GetQGANRealTrue(discWeights))
print("discriminator -  fake true: ", GetQGANFakeTrue(genWeights, discWeights))

print("Cost is: ", GetQGANDiscriminatorCost(discriminator_weights))
