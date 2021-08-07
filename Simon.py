# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile, assemble

# import basic plot tools
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# construct the oracle function for Simon's algorithm
def simon_oracle(b):
    n = len(b)
    
