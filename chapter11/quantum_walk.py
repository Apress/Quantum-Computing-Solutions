
import math
import pylab as pythonLab


def GetProbabilities(posn):
    
    return [sum([abs(amp) ** 2 for amp in place]) for place in posn]


def ApplyNormalisation(posn):
    
    N = math.sqrt(sum(GetProbabilities(posn)))
    return [[amp / N for amp in place] for place in posn]


def GetTimeStep(posn):
    
    return ApplyNormalisation([[x[0] + x[1], x[0] - x[1]] for x in posn])


def GetShift(coin):
    
    newposn = [[0, 0] for i in range(len(coin))]
    for j in range(1, len(position) - 1):
        newposn[j + 1][0] += coin[j][0]
        newposn[j - 1][1] += coin[j][1]
    return ApplyNormalisation(newposn)


minval, maxval = -400, 401
position = [[0, 0] for i in range(minval, maxval)]
position[-minval] = [1 / math.sqrt(2), 1j / math.sqrt(2)]

for time in range(-minval):
    position = GetShift(GetTimeStep(position))

pythonLab.plot(range(minval, maxval), GetProbabilities(position))
pythonLab.show()