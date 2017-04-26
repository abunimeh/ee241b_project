import os
import numpy as np
import bitarray

def prompt(message, errormessage, isvalid):
    """Prompt for input given a message and return that value after verifying the input.

    Keyword arguments:
    message -- the message to display when asking the user for the value
    errormessage -- the message to display when the value fails validation
    isvalid -- a function that returns True if the value given by the user is valid
    """
    res = None
    while res is None:
        res = raw_input(str(message)+': ')
        if not isvalid(res):
            print str(errormessage)
            res = None
    return res

def generate_sequences(num_sequences, num_vectors_per_sequence, output_directory_path, num_module_inputs, print_file_creation = False):
    leading_zeros = len(str(num_sequences-1))
    sequence_paths_file = open("%s/sequences" % (output_directory_path), "w")
    for sequence_idx in range(0, num_sequences):
        sequence_file_name = ("{0:0" + str(leading_zeros) + "}").format(sequence_idx)
        sequence_file_path = ("%s/%s" % (output_directory_path, sequence_file_name) )
        if print_file_creation:
            print(sequence_file_path)
        sequence_file = open(sequence_file_path, "w")
        for vector_idx in range(0, num_vectors_per_sequence):
            vector_bits = bitarray.bitarray((np.random.randn(num_module_inputs) > 0).tolist())
            sequence_file.write("%s\n" % vector_bits.to01())
        sequence_file.close()
        sequence_paths_file.write("%s\n" % os.path.abspath(sequence_file_path))
    sequence_paths_file.close()

def generate_testbench(inputs, outputs, module_name, vectors_per_sequence, sequence_paths, output_testbench_path):
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

        for sequence_file in sequence_paths:
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
