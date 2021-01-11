primes11={3,5,7,11,14};

primes12={3,5,7,11,13,17,19,34}

primes=primes11 & primes12

print("union of sets", primes11,",",primes12," is")
print(primes)


primes1={3,5,7,11,14};

primes2={3,5,7,11,13,17,19,34}

primes=primes1 & primes2

print("intersection of sets", primes1,",", primes2," is")
print(primes)



primes3={3,5,7,11,13,17,19}

primes4={2,3,5,7,11};

primes=primes3-primes4

print("difference of sets",primes3,",",primes4," is")

print(primes)


primes4={3,5,7,11,13,17,19}

primes5={3,5,7,11,91,101};

primes=primes4 ^ primes5

print("symmetric difference of sets",primes4,",",primes5," is")

print(primes)
