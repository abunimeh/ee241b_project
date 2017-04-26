#!/bin/bash
"""

python scripts/makefile_generator.py $module_name build-rvt/MakePowerEstimation
cd build-rvt/vcs-sim-rtl/
make clean
make
make run
"""
import sys
import shutil
import os
import numpy as np
import bitarray
# Custom imports
from verilog_parser import VerilogParser
import util

"""
This script will automate the flow of constructing a power model for a given 
combinational circuit. This script must be provided with certain parameters.
"""

# Parse command line arguments
if (len(sys.argv) != 4):
    print('Usage: python construct_power_model.py <Verilog module ' +  
            'name> <Number of sequences> <Number of vectors per sequence>')
    sys.exit(1)

verilog_module_name = sys.argv[1]
num_sequences = int(sys.argv[2])
num_vectors_per_sequence = int(sys.argv[3])
working_directory = os.path.abspath('../training_vectors/')
verilog_module_sources_directory = os.path.abspath('../iscas85_verilog/')
flow_sources_directory = os.path.abspath('../src/')

# Create working directory
print("Creating directory for test sequences to reside in at path: %s" % (os.path.abspath(working_directory)))
status = util.prompt(
        message = 'OK to wipe any existing directory? [Y/N]',
        errormessage = 'Enter a valid option',
        isvalid = lambda s: len(s) > 0)
if (status.upper() != 'Y'):
    sys.exit(0)

if os.path.isdir(working_directory):
    shutil.rmtree(working_directory)
os.mkdir(working_directory)

# Create Verilog parser for the target module
parser = VerilogParser(verilog_module_sources_directory + '/%s.v' % (verilog_module_name))

# Generate files for each test sequence
print("Generating %d sequences, each with %d test vectors" % (num_sequences, num_vectors_per_sequence))
print("Sequence files are being placed in %s" % (working_directory))
util.generate_sequences(num_sequences, num_vectors_per_sequence, working_directory, len(parser.inputs))

print("Removing all Verilog sources from flow directory: %s" % (flow_sources_directory))
# Remove all Verilog sources from the flow sources directory
for item in os.listdir(flow_sources_directory):
    if item.endswith('.v'):
        os.remove(os.path.join(flow_sources_directory, item))

print("Copying over Verilog module to flow directory %s" % (flow_sources_directory))
# Copy over Verilog module to the flow sources directory
shutil.copyfile('%s/%s.v' % (verilog_module_sources_directory, verilog_module_name),
        '%s/%s.v' % (flow_sources_directory, verilog_module_name))

# Create testbench
sequence_paths_filepath = '%s/sequences' % (working_directory) 
print("Reading sequences paths file at path %s" % (sequence_paths_filepath))
sequence_paths = []
with open(sequence_paths_filepath, 'r') as sequence_paths_file:
    for sequence_path in sequence_paths_file:
        sequence_paths.append(sequence_path.strip())

testbench_path = '%s/%s_tb.v' % (flow_sources_directory, parser.module_name)
print("Generating testbench at path %s" % (testbench_path))
        
util.generate_testbench(
        inputs = parser.inputs,
        outputs = parser.outputs,
        module_name = parser.module_name,
        sequence_paths = sequence_paths,
        vectors_per_sequence = num_vectors_per_sequence,
        output_testbench_path = testbench_path) 
