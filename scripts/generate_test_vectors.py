"""
This script will generate input test vectors to be driven into the DUT for the purpose
of creating the 4D table.

Calling Convention: python generate_test_vectors.py <circuit to test> <num_sequences> <num_vectors_per_sequence> <output directory>

Arguments:
    <circuit to test> = a relative or absolute path to a Verilog RTL file which will be used to automatically get number of inputs 
    <num sequences> = the number of test vector sequences to be generated (each one will have a separate file)
    <num vectors per sequence> = the number of input test vectors per sequence (this determines the resolution of the 
        4D table in the P_in and D_in and D_out axes)
    <output directory> = where to place a file for each test sequence, this directory will be created if it doesn't exist
        if the directory already exists all files inside it will be removed!
"""
import sys
import shutil
import os
import numpy as np
import bitarray
from verilog_parser import VerilogParser 

verilog_file_path = sys.argv[1]
num_sequences = int(sys.argv[2])
num_vectors_per_sequence = int(sys.argv[3])
output_directory_path = sys.argv[4]

parser = VerilogParser(verilog_file_path)
inputs = parser.inputs

print("Creating output directory (or cleaning it if already exists) at path: %s" % (output_directory_path))

if os.path.isdir(output_directory_path):
    shutil.rmtree(output_directory_path)
os.mkdir(output_directory_path)

print("Generating %d sequences, each with %d test vectors" % (num_sequences, num_vectors_per_sequence))

leading_zeros = len(str(num_sequences-1))
test_vector_file = open("%s/%s.txt" % (output_directory_path, output_directory_path), "w")
for sequence_idx in range(0, num_sequences):
    sequence_file_name = ("{0:0" + str(leading_zeros) + "}").format(sequence_idx)
    sequence_file_path = ("%s/%s.txt" % (output_directory_path, sequence_file_name) )
    print sequence_file_path
    sequence_file = open(sequence_file_path, "w")
    for vector_idx in range(0, num_vectors_per_sequence):
        vector_bits = bitarray.bitarray((np.random.randn(len(inputs)) > 0).tolist())
        sequence_file.write("%s\n" % vector_bits.to01())
    sequence_file.close()
    test_vector_file.write("%s\n" % os.path.abspath(sequence_file_path))
test_vector_file.close()
