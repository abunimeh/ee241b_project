import sys
import shutil
import os
import numpy as np
import bitarray
import subprocess
# Custom imports
from verilog_parser import VerilogParser
import util

"""
This script will automate the flow of constructing a power model for a given 
combinational circuit. This script must be provided with certain parameters.
"""

# Parse command line arguments
if (len(sys.argv) != 5):
    print('Usage: python gather_power_data.py <Verilog module ' +  
            'name> <Number of sequences> <Number of vectors per sequence> ' +
            '<working directory>')
    sys.exit(1)

verilog_module_name = sys.argv[1]
num_sequences = int(sys.argv[2])
num_vectors_per_sequence = int(sys.argv[3])
working_directory = os.path.abspath(sys.argv[4])
verilog_module_sources_directory = os.path.abspath('../iscas85_verilog/')
flow_sources_directory = os.path.abspath('../src/')
build_directory = os.path.abspath('../build-rvt/')
rtl_sim_directory = os.path.abspath('../build-rvt/vcs-sim-rtl/')
post_par_sim_directory = os.path.abspath('../build-rvt/vcs-sim-gl-par/')
primetime_directory = os.path.abspath('../build-rvt/pt-pwr/')
synthesis_directory = os.path.abspath('../build-rvt/dc-syn/')
par_directory = os.path.abspath('../build-rvt/icc-par/')

# Create working directory
print("Creating directory for test sequences to reside in at path: %s" % (os.path.abspath(working_directory)))
#status = util.prompt(
#        message = 'Should this directory be wiped? [Y/N]',
#        errormessage = 'Enter a valid option',
#        isvalid = lambda s: len(s) > 0)
new_working_directory = False
status = 'Y'
if (status.upper() == 'Y'):
    if os.path.isdir(working_directory):
        shutil.rmtree(working_directory)
    os.mkdir(working_directory)
    new_working_directory = True
else:
    new_working_directory = False

# Create Verilog parser for the target module
parser = VerilogParser(verilog_module_sources_directory + '/%s.v' % (verilog_module_name))

# Generate files for each test sequence
if new_working_directory:
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

    # Generate Makefrag
    makefrag_path = '%s/MakePowerEstimation' % (build_directory)
    print("Generating MakePowerEstimation at path %s" % (makefrag_path))
    util.generate_makefrag(
            module_name = parser.module_name,
            output_makefrag_path = makefrag_path)

    # Run RTL testbench using VCS
    subprocess.check_call(['cd %s && make clean' % (rtl_sim_directory)], shell = True)
    subprocess.check_call(['cd %s && make' % (rtl_sim_directory)], shell = True)
    subprocess.check_call(['cd %s && make run' % (rtl_sim_directory)], shell = True)

# Ask user if we should build the IC (synthesis + PAR). It is probably better that
# the user does this manually than through a script.
subprocess.check_call(['cd %s && make clean' % (synthesis_directory)], shell = True)
subprocess.check_call(['cd %s && make' % (synthesis_directory)], shell = True)

subprocess.check_call(['cd %s && make clean' % (par_directory)], shell = True)
subprocess.check_call(['cd %s && make' % (par_directory)], shell = True)

sequence_paths_filepath = '%s/sequences' % (working_directory) 
print("Reading sequences paths file at path %s" % (sequence_paths_filepath))
sequence_paths = []
with open(sequence_paths_filepath, 'r') as sequence_paths_file:
    for sequence_path in sequence_paths_file:
        sequence_paths.append(sequence_path.strip())

testbench_path = '%s/%s_tb.v' % (flow_sources_directory, parser.module_name)
# Create a new testbench per test sequence and run that testbench through the
# post-PAR VCS simulation
for sequence_path in sequence_paths:
    sequence_power_file = '%s/%s_pt_power' % (working_directory, os.path.basename(sequence_path))
    if os.path.isfile(sequence_power_file):
        continue
    util.generate_testbench(
            inputs = parser.inputs,
            outputs = parser.outputs,
            module_name = parser.module_name,
            sequence_paths = [sequence_path],
            vectors_per_sequence = num_vectors_per_sequence,
            output_testbench_path = testbench_path) 
    subprocess.check_call(['cd %s && make clean' % (post_par_sim_directory)], shell = True)
    subprocess.check_call(['cd %s && make' % (post_par_sim_directory)], shell = True)
    subprocess.check_call(['cd %s && make run' % (post_par_sim_directory)], shell = True)
    subprocess.check_call(['cd %s && make convert' % (post_par_sim_directory)], shell = True)

    # Now run the sequence through PrimeTime and save its output
    subprocess.check_call(['cd %s && make clean' % (primetime_directory)], shell = True)
    subprocess.check_call(['cd %s && make' % (primetime_directory)], shell = True)
    shutil.copyfile('%s/current-pt/reports/vcdplus.power.avg.max.report' % (primetime_directory), sequence_power_file)
