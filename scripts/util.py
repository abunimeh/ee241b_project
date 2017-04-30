import os
import numpy as np
import bitarray
from scipy.interpolate import griddata 
import itertools

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
    
    # For every sequence ...
    for sequence_idx in range(0, num_sequences):
        sequence_file_name = ("{0:0" + str(leading_zeros) + "}").format(sequence_idx)
        sequence_file_path = ("%s/%s" % (output_directory_path, sequence_file_name) )
        if print_file_creation:
            print(sequence_file_path)
        sequence_file = open(sequence_file_path, "w")

        # For num vectors per sequence ...
        seq_bits = generate_single_sequence(sequence_idx, num_sequences, num_vectors_per_sequence, num_module_inputs)
        for vector in seq_bits:
            sequence_file.write("%s\n" % vector.to01())

        sequence_file.close()
        sequence_paths_file.write("%s\n" % os.path.abspath(sequence_file_path))
    
    sequence_paths_file.close()

def generate_single_sequence(sequence_num, total_sequences, num_vectors_per_sequence, num_inputs):
    # Gradient of probability to generate an even Pin distribution (uniform)
    bit_prob = float(sequence_num) / float(total_sequences)
    sequence = []
    for vector_idx in range(0, num_vectors_per_sequence):
        vector_bits = bitarray.bitarray((np.random.rand(num_inputs) < bit_prob).tolist())
        sequence.append(vector_bits)

    return sequence

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
            tb_file.write('\t\t\t#5;\n')
            tb_file.write('\t\t\t// write dut_output to file\n')
            tb_file.write('\t\t\t$fwrite(f, "%b\\n", dut_output);\n')
            tb_file.write('\t\tend\n')
            tb_file.write('\t\t$fclose(f);\n\n')
        tb_file.write("\t\t$vcdplusoff;\n")
        tb_file.write("\t\t$finish();\n")
        tb_file.write("\tend\n")
        tb_file.write("endmodule\n")

def generate_makefrag(module_name, output_makefrag_path):
    with open(output_makefrag_path, "w") as makefrag_file:
        makefrag_file.write("vcs_rtl_vsrcs = \\\n")
        makefrag_file.write("   $(srcdir)/%s.v \\\n" % (module_name))
        makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (module_name))

        makefrag_file.write("\n")

        makefrag_file.write("vcs_syn_toplevel = %s\n" % (module_name))
        makefrag_file.write("vcs_syn_vsrcs = \\\n")
        makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (module_name))
        makefrag_file.write("   ../dc-syn/current-dc/results/$(toplevel).mapped.v \\\n")

        makefrag_file.write("\n")

        makefrag_file.write("dc_syn_toplevel = %s\n" % (module_name))
        makefrag_file.write("dc_syn_testharness = %s_tb\n" % (module_name))
        makefrag_file.write("dc_syn_toplevelinst = %s_inst\n" % (module_name))
        makefrag_file.write("dc_syn_vsrcs = \\\n")
        makefrag_file.write("   $(srcdir)/%s.v \\\n" % (module_name))

        makefrag_file.write("\n")

        makefrag_file.write("icc_par_toplevel = %s\n" % (module_name))
        makefrag_file.write("icc_par_testharness = %s_tb\n" % (module_name))
        makefrag_file.write("icc_par_toplevelinst = %s_inst\n" % (module_name))

        makefrag_file.write("\n")

        makefrag_file.write("vcs_par_toplevel = %s\n" % (module_name))
        makefrag_file.write("vcs_par_vsrcs = \\\n")
        makefrag_file.write("   $(srcdir)/%s_tb.v \\\n" % (module_name))
        makefrag_file.write("   ../icc-par/current-icc/results/$(toplevel).output.v \\\n")

        makefrag_file.write("\n")

        makefrag_file.write("pt_toplevel = %s\n" % (module_name))
        makefrag_file.write("pt_testharness = %s_tb\n" % (module_name))
        makefrag_file.write("pt_toplevelinst = %s_inst\n" % (module_name))

def compute_power(input_pt_file):
    contents = []
    with open(input_pt_file, 'r') as f:
        contents = f.readlines()
    power_string = [x.strip() for x in contents[-2].split(' ')]
    power_string = [x for x in power_string if x != ''] 
    power_string = power_string[1:5]
    power_string = [float(x) for x in power_string]
    return power_string[3]

def compute_input_statistics(input_sequence_file):
    input_vectors = []
    with open(input_sequence_file, 'r') as f:
        for line in f:
            bits = bitarray.bitarray(line.strip())
            input_vectors.append(bits)

    num_inputs = input_vectors[0].length()

    # Compute Pin for every input bit separately
    Pin = []
    for input_idx in range(0, num_inputs):
        high_values = 0
        for vector_idx in range(0, len(input_vectors)):
            if input_vectors[vector_idx][input_idx] == True:
                high_values = high_values + 1
        Pin.append(high_values / float(len(input_vectors)))

    # Compute Din for every input bit separately
    Din = []
    #for input_idx in range(0, num_inputs):
        

def compute_statistics(input_sequence_file, output_sequence_file):
    input_vectors = []
    output_vectors = []
    with open(input_sequence_file, 'r') as f:
        for line in f:
            bits = bitarray.bitarray(line.strip())
            input_vectors.append(bits)
    with open(output_sequence_file, 'r') as f:
        for line in f:
            bits = bitarray.bitarray(line.strip())
            output_vectors.append(bits)

    num_inputs = input_vectors[0].length()
    num_outputs = output_vectors[0].length()

    # Compute Pin (average input signal probability)
    total_row_pin = 0.0
    for input_vector in input_vectors:
        total_row_pin = total_row_pin + (float(input_vector.count(True)) / float(num_inputs))
    Pin = total_row_pin / float(len(input_vectors))

    # Compute Din (average input transition activity)
    total_transition_density = 0.0
    for idx in range(1, len(input_vectors)):
        transition_vector = input_vectors[idx-1] ^ input_vectors[idx]
        total_transition_density = total_transition_density + float(transition_vector.count(True)) / float(num_inputs)
    Din = total_transition_density / float(len(input_vectors) - 1)

    # Compute Dout (average output transition activity)
    total_transition_density = 0.0
    for idx in range(1, len(output_vectors)):
        transition_vector = output_vectors[idx-1] ^ output_vectors[idx]
        total_transition_density = total_transition_density + float(transition_vector.count(True)) / float(num_outputs)
    Dout = total_transition_density / float(len(output_vectors) - 1)

    # Compute SCin (average input spatial correlation coefficient)
    scin_total = 0.0
    for bit_idx1 in range(0, num_inputs):
        for bit_idx2 in range(bit_idx1 + 1, num_inputs):
            temp_sum = 0.0
            for time_idx in range(0, len(input_vectors)):
                vec = input_vectors[time_idx]
                if (vec[bit_idx1] == True) and (vec[bit_idx2] == True):
                    temp_sum = temp_sum + 1
            scin_total = scin_total + (float(temp_sum) / float(len(input_vectors)))
    SCin = scin_total * (2.0 / (num_inputs * (num_inputs-1)))
    
    return (Pin, Din, SCin, Dout)

"""
Given the 'statistics' for a particular sequence, construct the values that you can plug
into a linear model to compute the matrix multiplication.
"""
def construct_linear_vector(statistics):
    nested_vector = [[1.0], list(statistics)]
    # Flatten vector
    flat_vector =  list(itertools.chain.from_iterable(nested_vector))
    return flat_vector

"""
Given the 'statistics' for a particular sequence, construct the values to plug into a 
quadratic model. This involves the linear terms as well as cross terms and square terms.
"""
def construct_quadratic_vector(statistics):
    linear_vector = construct_linear_vector(statistics)
    quadratic_vector = []
    # Cross terms
    for i in range(0, len(statistics)):
        for j in range(i + 1, len(statistics)):
            quadratic_vector.append(statistics[i] * statistics[j])
    # Self-squared terms
    for i in range(0, len(statistics)):
        quadratic_vector.append(statistics[i] * statistics[i])
    # Flatten the 2 vectors combined
    flat_vector = list(itertools.chain.from_iterable([linear_vector, quadratic_vector])) 
    return flat_vector

"""
Given the 'statistics' for a particular sequence, construct the values to plug into a 
cubic model. This involves linear, quadratic, triple-cross terms, and self-cubed terms. 
"""
def construct_cubic_vector(statistics):
    quadratic_vector = construct_quadratic_vector(statistics)
    cubic_vector = []
    # Triplet - cross terms
    for subset in itertools.combinations(range(0, len(statistics)), 3):
        cubic_vector.append(reduce(lambda x,y: x*y, [statistics[i] for i in subset]))
    # Single term squared multiplied by 2 other terms
    for idx in range(0, len(statistics)):
        indices = list(range(0, len(statistics)))
        indices.remove(idx)
        for subset in itertools.combinations(indices, 2):
            cross_term = reduce(lambda x,y: x*y, [statistics[i] for i in subset])
            cubic_vector.append(cross_term * (statistics[idx]**2))
    # Self-cubed terms
    for idx in range(0, len(statistics)):
        cubic_vector.append(statistics[idx] * statistics[idx])
    # Flatten the 2 combined vectors
    flat_vector = list(itertools.chain.from_iterable([quadratic_vector, cubic_vector]))
    return flat_vector

def compute_4d_table_power_estimate(power_model, sequence_statistics):
    points = []
    values = []
    for statistics,power in power_model.iteritems():
        points.append(np.array(statistics))
        values.append(power)
    points = np.array(points)
    values = np.array(values)
    sequence_statistics = np.array(sequence_statistics)
    power_estimate_nn = griddata(points, values, sequence_statistics, method='nearest')
    power_estimate_linear = griddata(points, values, sequence_statistics, method='linear')
    for idx in range(0, len(power_estimate_linear)):
        if np.isnan(power_estimate_linear[idx]):
            power_estimate_linear[idx] = power_estimate_nn[idx]
    return power_estimate_linear

def compute_coeff_based_power_estimate(power_model, sequence_statistics, power_model_type):
    x = power_model
    A = []
    if power_model_type == 'linear':
        A = np.zeros((len(sequence_statistics), 5))
    elif power_model_type == 'quadratic':
        A = np.zeros((len(sequence_statistics), 15))
    elif power_model_type == 'cubic':
        A = np.zeros((len(sequence_statistics), 35))
    for idx in range(0, len(sequence_statistics)):
       if power_model_type == 'linear':
           A[idx] = construct_linear_vector(sequence_statistics[idx])
       elif power_model_type == 'quadratic':
           A[idx] = construct_quadratic_vector(sequence_statistics[idx])
       elif power_model_type == 'cubic':
           A[idx] = construct_cubic_vector(sequence_statistics[idx])
    return np.dot(A, x) 

