import numpy as np
from math import gcd
from numpy.random import randint
import pandas as pd
from fractions import Fraction
# importing Qiskit
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
# import basic plot tools
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
# import inverse Quantum Fourier Transform
from QuantumFourierTransform import QFourier_inverse


# U |y> = |ay mod 15>
def c_amod15(a, power):
    """ Controlled multiplication by a mod 15 """
    """ Returns the controlled-U gate for a, repeated power times """
    if a not in [2,7,8,11,13]:
        raise ValueError("'a' must be 2,7,8,11 or 13")
    U = QuantumCircuit(4)        
    for iteration in range(power):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a == 11:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "%i^%i mod 15" % (a, power)
    c_U = U.control()
    return c_U


def periodfinding_demonstration():
    # Specify variables
    n_count = 3  # number of counting qubits
    a = 7
    # Create QuantumCircuit with n_count counting qubits
    # plus 4 qubits for U to act on
    qc = QuantumCircuit(n_count + 4, n_count)

    # Initialize counting qubits
    # in state |+>
    for q in range(n_count):
        qc.h(q)
    qc.barrier()
    
    # And auxiliary register in state |1>
    qc.x(3 + n_count)
    qc.barrier()

    # Do controlled-U operations
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + [i+n_count for i in range(4)])
    qc.barrier()

    # Do inverse-QFT
    QFourier_inverse(qc, n_count)

    # Measure circuit
    qc.measure(range(n_count), range(n_count))
    qc.draw(fold=-1, output='mpl')  # -1 means 'do not fold' 
    plt.show()

    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc)
    results = aer_sim.run(qobj).result()
    counts = results.get_counts()
    plot_histogram(counts)
    plt.show()

    rows, measured_phases = [], []
    for output in counts:
        decimal = int(output, 2)  # Convert (base 2) string to decimal
        phase = decimal/(2**n_count)  # Find corresponding eigenvalue
        measured_phases.append(phase)
        # Add these values to the rows in our table:
        rows.append([f"{output}(bin) = {decimal:>3}(dec)", 
                    f"{decimal}/{2**n_count} = {phase:.2f}"])
    # Print the rows in a table
    headers=["Register Output", "Phase"]
    df = pd.DataFrame(rows, columns=headers)
    print(df)

    rows = []
    for phase in measured_phases:
        frac = Fraction(phase).limit_denominator(15)
        rows.append([phase, f"{frac.numerator}/{frac.denominator}", frac.denominator])
    # Print as a table
    headers=["Phase", "Fraction", "Guess for r"]
    df = pd.DataFrame(rows, columns=headers)
    print(df)

    return None


if __name__ == '__main__':
    
    periodfinding_demonstration()

