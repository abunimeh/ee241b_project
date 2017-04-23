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
import re

verilog_file_path = sys.argv[1]
num_sequences = sys.argv[2]
num_vectors_per_sequence = sys.argv[3]
output_directory_path = sys.argv[4]

# Get a listing of the inputs for the circuit as described in the Verilog file
# Note that this assumes the Verilog-2001 way of declaring inputs
"""
module asdf (N1, N2, N3, ...);

input N1, N2,
    N3;
"""
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w)).search

input_string = ""
input_section = False
print("Parsing Verilog file at path: %s" % (verilog_file_path))
with open(verilog_file_path, 'r') as f:
    for line in f:
        if input_section:
            input_string = input_string + line
        if findWholeWord('input')(line):
            input_section = True
            input_string = input_string + line
        if ';' in line and input_section == True:
            break

input_string = input_string.strip()
input_string = input_string.replace('\r', '')
input_string = input_string.replace('\n', '')
input_string = input_string.replace(' ', '')
input_string = input_string.replace('input', '')
input_string = input_string.replace(';', '')
inputs = input_string.split(',')

print("Found these inputs to the Verilog module: %s" % (inputs))
print("Num inputs: %d" % (len(inputs)))

print("Creating output directory (or cleaning it if already exists) at path: %s" % (output_directory_path))


