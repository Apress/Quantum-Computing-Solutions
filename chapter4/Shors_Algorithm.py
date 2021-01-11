import math
import random



class QuantumMap:
	def __init__(self, state, amplitude):
		self.state = state
		self.amplitude = amplitude


class QuantumEntanglement:
	def __init__(self, amplitude, register):
		self.amplitude = amplitude
		self.register = register
		self.entangled = {}

	def UpdateEntangled(self, fromState, amplitude):
		register = fromState.register
		entanglement = QuantumMap(fromState, amplitude)
		try:
			self.entangled[register].append(entanglement)
		except KeyError:
			self.entangled[register] = [entanglement]

	def RetrieveEntangles(self, register = None):
		entangles = 0
		if register is None:
			for states in self.entangled.values():
				entangles += len(states)
		else:
			entangles = len(self.entangled[register])

		return entangles


class QuantumRecord:
	def __init__(self, numBits):
		self.numBits = numBits
		self.numStates = 1 << numBits
		self.entangled = []
		self.states = [QuantumEntanglement(complex(0.0), self) for x in range(self.numStates)]
		self.states[0].amplitude = complex(1.0)

	def UpdatePropagate(self, fromRegister = None):
		if fromRegister is not None:
			for state in self.states:
				amplitude = complex(0.0)

				try:
					entangles = state.entangled[fromRegister]
					for entangle in entangles:
						amplitude += entangle.state.amplitude * entangle.amplitude

					state.amplitude = amplitude
				except KeyError:
					state.amplitude = amplitude

		for register in self.entangled:
			if register is fromRegister:
				continue

			register.UpdatePropagate(self)

	def UpdateMap(self, toRegister, mapping, propagate = True):
		self.entangled.append(toRegister)
		toRegister.entangled.append(self)

		mapTensorX = {}
		mapTensorY = {}
		for x in range(self.numStates):
			mapTensorX[x] = {}
			codomain = mapping(x)
			for element in codomain:
				y = element.state
				mapTensorX[x][y] = element

				try:
					mapTensorY[y][x] = element
				except KeyError:
					mapTensorY[y] = { x: element }

		def UpdateNormalize(tensor, p = False):
			lSqrt = math.sqrt
			for vectors in tensor.values():
				sumProb = 0.0
				for element in vectors.values():
					amplitude = element.amplitude
					sumProb += (amplitude * amplitude.conjugate()).real

				normalized = lSqrt(sumProb)
				for element in vectors.values():
					element.amplitude = element.amplitude / normalized

		UpdateNormalize(mapTensorX)
		UpdateNormalize(mapTensorY, True)

		for x, yStates in mapTensorX.items():
			for y, element in yStates.items():
				amplitude = element.amplitude
				toState = toRegister.states[y]
				fromState = self.states[x]
				toState.UpdateEntangled(fromState, amplitude)
				fromState.UpdateEntangled(toState, amplitude.conjugate())

		if propagate:
			toRegister.UpdatePropagate(self)

	def RetrieveMeasure(self):
		measure = random.random()
		sumProb = 0.0

		# Pick a state
		finalX = None
		finalState = None
		for x, state in enumerate(self.states):
			amplitude = state.amplitude
			sumProb += (amplitude * amplitude.conjugate()).real

			if sumProb > measure:
				finalState = state
				finalX = x
				break

		if finalState is not None:
			for state in self.states:
				state.amplitude = complex(0.0)

			finalState.amplitude = complex(1.0)
			self.UpdatePropagate()

		return finalX

	def RetrieveEntangles(self, register = None):
		entangles = 0
		for state in self.states:
			entangles += state.entangles(None)

		return entangles

	def RetrieveAmplitudes(self):
		amplitudes = []
		for state in self.states:
			amplitudes.append(state.amplitude)

		return amplitudes

def FindListEntangles(register):
	print("Entangles: " + str(register.RetrieveEntangles()))

def FindListAmplitudes(register):
	amplitudes = register.amplitudes()
	for x, amplitude in enumerate(amplitudes):
		print('State #' + str(x) + '\'s Amplitude value: ' + str(amplitude))

def InvokeHadamard(x, Q):
	codomain = []
	for y in range(Q):
		amplitude = complex(pow(-1.0, RetrieveBitCount(x & y) & 1))
		codomain.append(QuantumMap(y, amplitude))

	return  codomain

def InvokeQModExp(a, exp, mod):
	state = InvokeModExp(a, exp, mod)
	amplitude = complex(1.0)
	return [QuantumMap(state, amplitude)]

def InvokeQft(x, Q):
	fQ = float(Q)
	k = -2.0 * math.pi
	codomain = []

	for y in range(Q):
		theta = (k * float((x * y) % Q)) / fQ
		amplitude = complex(math.cos(theta), math.sin(theta))
		codomain.append(QuantumMap(y, amplitude))

	return codomain

def DeterminePeriod(a, N):
	nNumBits = N.bit_length()
	inputNumBits = (2 * nNumBits) - 1
	inputNumBits += 1 if ((1 << inputNumBits) < (N * N)) else 0
	Q = 1 << inputNumBits

	print("The period is...")
	print("Q = " + str(Q) + "\ta = " + str(a))
	
	inputRegister = QuantumRecord(inputNumBits)
	hmdInputRegister = QuantumRecord(inputNumBits)
	qftInputRegister = QuantumRecord(inputNumBits)
	outputRegister = QuantumRecord(inputNumBits)

	print("Registers are instantiated")
	print("Executing Hadamard on the input")

	inputRegister.UpdateMap(hmdInputRegister, lambda x: InvokeHadamard(x, Q), False)

	print("Hadamard operation is invoked")
	print("Mapping input register to the output")

	hmdInputRegister.UpdateMap(outputRegister, lambda x: InvokeQModExp(a, x, N), False)

	print("Modular exponentiation is invoked")
	print("Executing quantum Fourier transform on the output")

	hmdInputRegister.UpdateMap(qftInputRegister, lambda x: InvokeQft(x, Q), False)
	inputRegister.UpdatePropagate()

	print("Quantum Fourier transform is invoked")
	print("Retrieving a measurement on the output")

	y = outputRegister.RetrieveMeasure()

	print("Measuring the Output register \ty = " + str(y))


	print("Retrieving  a measurement on the periodicity")

	x = qftInputRegister.RetrieveMeasure()

	print("Measuring QFT  \tx = " + str(x))

	if x is None:
		return None

	print("Retrieving the period via continued fractions")

	r = RetrieveContinuedFraction(x, Q, N)

	print("Determined Candidate period\tr = " + str(r))

	return r



def RetrieveBitCount(x):
	sumBits = 0
	while x > 0:
		sumBits += x & 1
		x >>= 1

	return sumBits

def RetrieveGcd(a, b):
	while b != 0:
		tA = a % b
		a = b
		b = tA

	return a

def RetrieveExtendedGCD(a, b):
	fractions = []
	while b != 0:
		fractions.append(a // b)
		tA = a % b
		a = b
		b = tA

	return fractions

def RetrieveContinuedFraction(y, Q, N):
	fractions = RetrieveExtendedGCD(y, Q)
	depth = 2

	def RetrievePartial(fractions, depth):
		c = 0
		r = 1

		for i in reversed(range(depth)):
			tR = fractions[i] * r + c
			c = r
			r = tR

		return c

	r = 0
	for d in range(depth, len(fractions) + 1):
		tR = RetrievePartial(fractions, d)
		if tR == r or tR >= N:
			return r

		r = tR

	return r

def InvokeModExp(a, exp, mod):
	fx = 1
	while exp > 0:
		if (exp & 1) == 1:
			fx = fx * a % mod
		a = (a * a) % mod
		exp = exp >> 1

	return fx

def RetrieveRandom(N):
	a = math.floor((random.random() * (N - 1)) + 0.5)
	return a

def RetrieveNeighBorCandidates(a, r, N, neighborhood):
	if r is None:
		return None

	for k in range(1, neighborhood + 2):
		tR = k * r
		if InvokeModExp(a, a, N) == InvokeModExp(a, a + tR, N):
			return tR

	for tR in range(r - neighborhood, r):
		if InvokeModExp(a, a, N) == InvokeModExp(a, a + tR, N):
			return tR

	for tR in range(r + 1, r + neighborhood + 1):
		if InvokeModExp(a, a, N) == InvokeModExp(a, a + tR, N):
			return tR

	return None

def ExecuteShorsAlgorithm(N, attempts = 1, neighborhood = 0.0, numPeriods = 1):
    
	periods = []
	neighborhood = math.floor(N * neighborhood) + 1

	print("N value is" + str(N))
	print("Neighborhood value is = " + str(neighborhood))
	print("Number of periods is = " + str(numPeriods))

	for attempt in range(attempts):
		print("\nAttempt #" + str(attempt))

		a = RetrieveRandom(N)
		while a < 2:
			a = RetrieveRandom(N)

		d = RetrieveGcd(a, N)
		if d > 1:
			print("Determined factors classically, re-attempt")
			continue

		r = DeterminePeriod(a, N)

		print("validating the candidate period, nearby values, and multiples")

		r = RetrieveNeighBorCandidates(a, r, N, neighborhood)

		if r is None:
			print("Period was not determined, re-attempt")
			continue

		if (r % 2) > 0:
			print("Period is odd, re-attempt")
			continue

		d = InvokeModExp(a, (r // 2), N)
		if r == 0 or d == (N - 1):
			print("Period is trivial, re-attempt")
			continue

		print("Period found\tr = " + str(r))

		periods.append(r)
		if(len(periods) < numPeriods):
			continue

		print("\n Determining  least common multiple of all periods")

		r = 1
		for period in periods:
			d = RetrieveGcd(period, r)
			r = (r * period) // d

		b = InvokeModExp(a, (r // 2), N)
		f1 = RetrieveGcd(N, b + 1)
		f2 = RetrieveGcd(N, b - 1)

		return [f1, f2]

	return None


results = ExecuteShorsAlgorithm(35, 20, 0.01, 2)
print("Results are:\t" + str(results[0]) + ", " + str(results[1]))

