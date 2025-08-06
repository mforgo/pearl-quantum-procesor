import numpy as np
from src.procesor import Procesor

@pytest.fixture
def qcpu():
    q = Procesor(mode="quantum", debug=False)
    # override small quantum register for test clarity
    q.quantum_registers.reset()
    return q

def test_hadamard_and_measure(qcpu):
    # Apply H on q0 -> equal superposition
    qcpu._execute_h(["q0"])
    state = qcpu.quantum_registers.get_full_state()
    # amplitude of |0> and |1> are ±1/√2
    amp0 = state[0]; amp1 = state[1]
    assert np.isclose(abs(amp0),1/np.sqrt(2))
    assert np.isclose(abs(amp1),1/np.sqrt(2))
    # Measure q0 many times approximates 50/50
    counts = {0:0,1:0}
    for _ in range(1000):
        qcpu.quantum_registers.reset(); qcpu._execute_h(["q0"])
        result = qcpu.quantum_registers.measure(0)
        counts[result]+=1
    assert 400 < counts[0] < 600  # roughly balanced

def test_cnot_entanglement(qcpu):
    # Create Bell pair
    qcpu._execute_bell(["q0","q1"])
    # Measure both qubits repeatedly -> always same result
    for _ in range(50):
        qcpu.quantum_registers.reset()
        qcpu._execute_bell(["q0","q1"])
        r0 = qcpu.quantum_registers.measure(0)
        r1 = qcpu.quantum_registers.measure(1)
        assert r0 == r1
