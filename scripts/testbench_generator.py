"""
This script will generate a Verilog testbench for a given Verilog module.
The testbench will inject test vectors into the module and will print out
the output of the module for a given test vector to a file.

Calling Convention: python testbench_generator.py <circuit to test> <test sequences file> <test vectors per sequence> <output testbench path and filename>

Arguments:
    <circuit to test> = a relative or absolute path to a Verilog RTL file which will be parsed to get the module name, inputs and outputs
    <test sequences file> = a relative or absolute path to a file which CONTAINS one or more absolute paths to files that contain test vectors
    <test vectors per sequence> = each sequence file contains this number of test vectors
    <output testbench path and filename> = a relative or absolute path to where the testbench should be written to
"""
import sys
import shutil
import os
import bitarray
from verilog_parser import VerilogParser

verilog_file_path = sys.argv[1]
test_sequences_file_path = sys.argv[2]
vectors_per_sequence = int(sys.argv[3])
output_testbench_path = sys.argv[4]

# Parse the Verilog RTL file
parser = VerilogParser(verilog_file_path)
inputs = parser.inputs
outputs = parser.outputs
module_name = parser.moduleName

with open(output_testbench_path, "w") as tb_file:
    tb_file.write("`timescale 1ns/1ps\n")
    tb_file.write("module %s_tb();\n\n" % (module_name))

    # Create a wire for the DUT's output
    tb_file.write("\twire [%d:0] dut_output;\n" % (len(outputs) - 1))

    # Create a test vector reg for the test vectors contained in each sequence file
    tb_file.write("\treg [%d:0] testvector [0:%d];\n" % ((len(inputs) - 1), vectors_per_sequence-1))

    # Create a reg for the inputs of the DUT
    tb_file.write("\treg [%d:0] dut_input;\n\n" % (len(inputs) - 1))

    # Instantiate and wire up the DUT
    tb_file.write("\t%s %s_inst (\n" % (module_name, module_name))
    tb_file.write("\t\t// DUT Inputs\n") 
    for input_idx in range(0, len(inputs)):
        tb_file.write("\t\t.%s(dut_input[%d]),\n" % (inputs[input_idx], input_idx))
    tb_file.write("\t\t// DUT Outputs\n")
    for output_idx in range(0, len(outputs)):
        if (output_idx == len(outputs) - 1):
            tb_file.write("\t\t.%s(dut_output[%d])\n" % (outputs[output_idx], output_idx))
        else:
            tb_file.write("\t\t.%s(dut_output[%d]),\n" % (outputs[output_idx], output_idx))
    tb_file.write("\t);\n\n")

    # Create the testvector's looping integer, the file pointer and the initial block
    tb_file.write("\tinteger i;\n\tinteger f;\n\n")
    tb_file.write("\tinitial begin\n")
    tb_file.write("\t$vcdpluson;\n")    

    with open(test_sequences_file_path, "r") as test_sequences_file:
        for sequence_file in test_sequences_file:
            sequence_file = sequence_file.strip()
            tb_file.write('\t\t$readmemb("%s", testvector);\n' % (sequence_file))
            tb_file.write('\t\tf = $fopen("%s", "w");\n' % (sequence_file + '_out'))
            tb_file.write('\t\tfor(i = 0; i < %d; i = i + 1) begin\n' % (vectors_per_sequence))
            tb_file.write('\t\t\tdut_input = testvector[i];\n')
            tb_file.write('\t\t\t#1;\n')
            tb_file.write('\t\t\t// write dut_output to file\n')
            tb_file.write('\t\t\t$fwrite(f, "%b\\n", dut_output);\n')
            tb_file.write('\t\tend\n')
            tb_file.write('\t\t$fclose(f);\n\n')
    tb_file.write("\t\t$vcdplusoff;\n")
    tb_file.write("\t\t$finish();\n")
    tb_file.write("\tend\n")
    tb_file.write("endmodule\n")
