
from collections import defaultdict

import numpy as nump
from mock import patch

from collections import defaultdict
from operator import xor
from typing import Dict, Tuple, List
import numpy.random as rand

from pyquil import Program
from pyquil.api import QuantumComputer
from pyquil.gates import H, MEASURE


def RetrieveOnetoOneMap(mask: str) -> Dict[str, str]:
    n_bits = len(mask)
    form_string = "{0:0" + str(n_bits) + "b}"
    bit_map_dct = {}
    for idx in range(2**n_bits):
        bit_string = form_string.format(idx)
        bit_map_dct[bit_string] = InvokeBitwiseXorOperation(bit_string, mask)
    return bit_map_dct


def RetrieveValidTwotoOneMap(mask: str, random_seed: int = None) -> Dict[str, str]:
    if random_seed is not None:
        rand.seed(random_seed)
    bit_map = RetrieveOnetoOneMap(mask)
    n_samples = int(len(bit_map.keys()) / 2)

    range_of_2to1_map = list(rand.choice(list(sorted(bit_map.keys())), replace=False, size=n_samples))

    list_of_bitstring_tuples = sorted([(k, v) for k, v in bit_map.items()], key=lambda x: x[0])

    bit_map_dct = {}
    for cnt in range(n_samples):
        bitstring_tup = list_of_bitstring_tuples[cnt]
        val = range_of_2to1_map[cnt]
        bit_map_dct[bitstring_tup[0]] = val
        bit_map_dct[bitstring_tup[1]] = val

    return bit_map_dct


class Simons_Algorithm(object):
    def __init__(self):
        self.unitary_function_mapping = None
        self.n_qubits = None
        self.n_ancillas = None
        self._qubits = None
        self.computational_qubits = None
        self.ancillas = None
        self.simon_circuit = None
        self._dict_of_linearly_indep_bit_vectors = {}
        self.search_mask = None
        self.bit_map = None
        self.classical_register = None

    def RetrieveSimonCircuit(self) -> Program:
        simon_circuit = Program()

        oracle_name = "SIMON_ORACLE_FUNCTION"
        simon_circuit.defgate(oracle_name, self.unitary_function_mapping)

        simon_circuit.inst([H(i) for i in self.computational_qubits])
        simon_circuit.inst(tuple([oracle_name] + sorted(self._qubits, reverse=True)))
        simon_circuit.inst([H(i) for i in self.computational_qubits])
        return simon_circuit

    def _Initialize_Attributes(self, bitstring_map: Dict[str, str]) -> None:
        self.bit_map = bitstring_map
        self.n_qubits = len(list(bitstring_map.keys())[0])
        self.n_ancillas = self.n_qubits
        self._qubits = list(range(self.n_qubits + self.n_ancillas))
        self.computational_qubits = self._qubits[:self.n_qubits]
        self.ancillas = self._qubits[self.n_qubits:]
        self.unitary_function_mapping, _ = self.CalculateUnitaryOracle(bitstring_map)
        self.simon_circuit = self.RetrieveSimonCircuit()
        self._dict_of_linearly_indep_bit_vectors = {}
        self.search_mask = None

    @staticmethod
    def CalculateUnitaryOracle(bitstring_map: Dict[str, str]) -> Tuple[nump.ndarray,Dict[str, str]]:
        n_bits = len(list(bitstring_map.keys())[0])

        ufunc = nump.zeros(shape=(2 ** (2 * n_bits), 2 ** (2 * n_bits)))
        index_mapping_dct = defaultdict(dict)
        for b in range(2**n_bits):
            pad_str = nump.binary_repr(b, n_bits)
            for k, v in bitstring_map.items():
                index_mapping_dct[pad_str + k] = InvokeBitwiseXorOperation(pad_str, v) + k
                i, j = int(pad_str+k, 2), int(InvokeBitwiseXorOperation(pad_str, v) + k, 2)
                ufunc[i, j] = 1
        return ufunc, index_mapping_dct

    def RetrieveBitMask(self, qc: QuantumComputer, bitstring_map: Dict[str, str]) -> str:
        self._Initialize_Attributes(bitstring_map)

        self.RetrieveSampleIndependentBits(qc)
        self.RetrieveInverseMaskEquation()

        if self.CheckValidMaskIfCorrect():
            return self.search_mask
        else:
            raise Exception("No valid mask found")

    def RetrieveSampleIndependentBits(self, quantum_computer: QuantumComputer) -> None:
        while len(self._dict_of_linearly_indep_bit_vectors) < self.n_qubits - 1:

            prog = Program()
            simon_ro = prog.declare('ro', 'BIT', len(self.computational_qubits))
            prog += self.simon_circuit
            prog += [MEASURE(qubit, ro) for qubit, ro in zip(self.computational_qubits, simon_ro)]
            executable = quantum_computer.compile(prog)
            sampled_bit_string = nump.array(quantum_computer.run(executable)[0], dtype=int)

            self.AppendToDictofIndepBits(sampled_bit_string)

    def RetrieveInverseMaskEquation(self) -> None:
        missing_msb = self.RetrieveMissingMsbVector()
        upper_triangular_matrix = nump.asarray(
            [tup[1] for tup in sorted(zip(self._dict_of_linearly_indep_bit_vectors.keys(),
                                          self._dict_of_linearly_indep_bit_vectors.values()),
                                      key=lambda x: x[0])])

        msb_unit_vec = nump.zeros(shape=(self.n_qubits,), dtype=int)
        msb_unit_vec[missing_msb] = 1

        self.search_mask = RetrieveBinaryBackSubstitute(upper_triangular_matrix, msb_unit_vec).tolist()

    def AppendToDictofIndepBits(self, z: nump.ndarray) -> None:
        if (z == 0).all() or (z == 1).all():
            return None
        msb_z = RetrieveMostSignificantBit(z)

        if msb_z not in self._dict_of_linearly_indep_bit_vectors.keys():
            self._dict_of_linearly_indep_bit_vectors[msb_z] = z
        else:
            conflict_z = self._dict_of_linearly_indep_bit_vectors[msb_z]
            not_z = [xor(conflict_z[idx], z[idx]) for idx in range(len(z))]
            if (nump.asarray(not_z) == 0).all():
                return None
            msb_not_z = most_significant_bit(nump.asarray(not_z))
            if msb_not_z not in self._dict_of_linearly_indep_bit_vectors.keys():
                self._dict_of_linearly_indep_bit_vectors[msb_not_z] = not_z

    def RetrieveMissingMsbVector(self) -> int:
        missing_msb = None
        for idx in range(self.n_qubits):
            if idx not in self._dict_of_linearly_indep_bit_vectors.keys():
                missing_msb = idx

        if missing_msb is None:
            raise ValueError("Expected a missing provenance, but didn't find one.")

        augment_vec = nump.zeros(shape=(self.n_qubits,))
        augment_vec[missing_msb] = 1
        self._dict_of_linearly_indep_bit_vectors[missing_msb] = augment_vec.astype(int).tolist()
        return missing_msb

    def CheckValidMaskIfCorrect(self) -> bool:
        mask_str = ''.join([str(b) for b in self.search_mask])
        return all([self.bit_map[k] == self.bit_map[InvokeBitwiseXorOperation(k, mask_str)]
                    for k in self.bit_map.keys()])

PADDED_BINARY_BIT_STRING = "{0:0{1:0d}b}"


def CheckValidIfUnitary(matrix: nump.ndarray) -> bool:
    rows, cols = matrix.shape
    if rows != cols:
        return False
    return nump.allclose(nump.eye(rows), matrix.dot(matrix.T.conj()))


def RetrieveMostSignificantBit(lst: nump.ndarray) -> int:
    return nump.argwhere(nump.asarray(lst) == 1)[0][0]


def InvokeBitwiseXorOperation(bs0: str, bs1: str) -> str:
    if len(bs0) != len(bs1):
        raise ValueError("Bit strings are not of equal length")
    n_bits = len(bs0)
    return PADDED_BINARY_BIT_STRING.format(xor(int(bs0, 2), int(bs1, 2)), n_bits)


def RetrieveBinaryBackSubstitute(W: nump.ndarray, s: nump.ndarray) -> nump.ndarray:
    m = nump.copy(s)
    n = len(s)
    for row_num in range(n - 2, -1, -1):
        row = W[row_num]
        for col_num in range(row_num + 1, n):
            if row[col_num] == 1:
                m[row_num] = xor(s[row_num], s[col_num])

    return m[::-1]



search_mask = '110'
bm = RetrieveValidTwotoOneMap(search_mask, random_seed=42)
expected_map = {
    '000': '001',
    '001': '101',
    '010': '000',
    '011': '111',
    '100': '000',
    '101': '111',
    '110': '001',
    '111': '101'
}
for k, v in bm.items():
    assert v == expected_map[k]


reverse_bitmap = defaultdict(list)
for k, v in bm.items():
    reverse_bitmap[v].append(k)

expected_reverse_bitmap = {
    '001': ['000', '110'],
    '101': ['001', '111'],
    '000': ['010', '100'],
    '111': ['011', '101']
}

for k, v in reverse_bitmap.items():
    assert sorted(v) == sorted(expected_reverse_bitmap[k])




with patch("pyquil.api.QuantumComputer") as quantum_computer:
    quantum_computer.run.side_effect = [
        (nump.asarray([0, 1, 1], dtype=int), ),
        (nump.asarray([1, 1, 1], dtype=int), ),
        (nump.asarray([1, 1, 1], dtype=int), ),
        (nump.asarray([1, 0, 0], dtype=int), ),
    ]


simon_algo = Simons_Algorithm()
result_mask = simon_algo.RetrieveBitMask(quantum_computer, bm)
print("mask", search_mask," result mask",result_mask)
