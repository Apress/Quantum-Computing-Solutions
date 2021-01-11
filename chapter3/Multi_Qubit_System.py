import math
import random

def ApplyCNOTQuantumGate(zerozero,zeroone,onezero,oneone):
    onezero, oneone = oneone, onezero
    return GetQuantumbits(zerozero,zeroone,onezero,oneone)

def ApplyHQuantumGate(zerozero,zeroone,onezero,oneone):
    a = zerozero
    b = zeroone
    c = onezero
    d = oneone

    zerozero = a + c
    zeroone  = b + d
    onezero  = a - c
    oneone   = b - d

    normalize()

    return GetQuantumbits(zerozero,zeroone,onezero,oneone)

def ApplyXQuantumGate(zerozero,zeroone,onezero,oneone):
    a = zerozero
    b = zeroone
    c = onezero
    d = oneone

    zerozero = c
    zeroone  = d
    onezero  = a
    oneone   = b

    return GetQuantumbits(zerozero,zeroone,onezero,oneone)

def ApplyZQuantumGate(zerozero,zeroone,onezero,oneone):
    onezero *= -1
    oneone  *= -1

    return GetQuantumbits(zerozero,zeroone,onezero,oneone)

def ApplyNormalization(zerozero,zeroone,onezero,oneone):
    norm = (abs(zerozero) ** 2 + abs(zeroone) ** 2 +
            abs(onezero) ** 2 + abs(oneone) ** 2) ** 0.5
    zerozero /= norm
    zeroone  /= norm
    onezero  /= norm
    oneone   /= norm
    return GetQuantumbits(zerozero,zeroone,onezero,oneone)

def MeasureQuantumbit(zerozero,zeroone,onezero,oneone):
    zerozeroprob = abs(zerozero) ** 2
    zerooneprob  = abs(zeroone)  ** 2
    onezeroprob  = abs(onezero)  ** 2
    randomchoice = random.random()

    if randomchoice < zerozeroprob:
        zerozero = complex(1)
        zeroone  = complex(0)
        onezero  = complex(0)
        oneone   = complex(0)
        return (0, 0)
    elif randomchoice < zerooneprob:
        zerozero = complex(0)
        zeroone  = complex(1)
        onezero  = complex(0)
        oneone   = complex(0)
        return (0, 1)
    elif randomchoice < onezeroprob:
        zerozero = complex(0)
        zeroone  = complex(0)
        onezero  = complex(1)
        oneone   = complex(0)
        return (1, 0)
    else:
        zerozero = complex(0)
        zeroone  = complex(0)
        onezero  = complex(0)
        oneone   = complex(1)
        return (1, 1)
    
def GetQuantumbits(zerozero,zeroone,onezero,oneone):
    comp = [zerozero, zeroone, onezero, oneone]
    comp = [i.real if i.real == i else i for i in comp]
    comp = [str(i) for i in comp]
    comp = ["" if i == "1.0" else i for i in comp]

    ls = []
    if abs(zerozero) > 0:
        ls += [comp[0] + " |00>"] 
    if abs(zeroone)  > 0:
        ls += [comp[1] + " |01>"] 
    if abs(onezero)  > 0:
        ls += [comp[2]  + " |10>"] 
    if abs(oneone)   > 0:
        ls += [comp[3]   + " |11>"] 

    comp = " + ".join(ls)

    return comp
        
a_quantum_state = 1
b_quantum_state = 0
c_quantum_state = 0
d_quantum_state = 0
zerozero_quantum_state = complex(a_quantum_state)
zeroone_quantum_state  = complex(b_quantum_state)
onezero_quantum_state  = complex(c_quantum_state)
oneone_quantum_state   = complex(d_quantum_state)     
result1 = ApplyCNOTQuantumGate(zerozero_quantum_state,zeroone_quantum_state,onezero_quantum_state,oneone_quantum_state)
print("cnot gate operation - result",result1)
result2 = ApplyXQuantumGate(zerozero_quantum_state,zeroone_quantum_state,onezero_quantum_state,oneone_quantum_state)
print("xgate operation - result",result2)
result3 = ApplyZQuantumGate(zerozero_quantum_state,zeroone_quantum_state,onezero_quantum_state,oneone_quantum_state)
print("zgate operation - result",result3)
result4 = ApplyNormalization(zerozero_quantum_state,zeroone_quantum_state,onezero_quantum_state,oneone_quantum_state)
print("normalize operation - result",result4)
result5 = MeasureQuantumbit(zerozero_quantum_state,zeroone_quantum_state,onezero_quantum_state,oneone_quantum_state)
print("measure gate operation - result",result5)
