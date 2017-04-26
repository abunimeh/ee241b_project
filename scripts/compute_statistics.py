"""
Given a sequence input and sequence output file, this script will compute the 
statistics for the 4D table (Pin, Din, SCin, Dout)
"""
from bitarray import bitarray
def compute_statistics(input_sequence_file, output_sequence_file):
    input_vectors = []
    output_vectors = []
    with open(input_sequence_file, 'r') as f:
        for line in f:
            bits = bitarray(line.strip())
            input_vectors.append(bits)
    with open(output_sequence_file, 'r') as f:
        for line in f:
            bits = bitarray(line.strip())
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
            for time_idx in range(0, len(input_vectors)):
                temp_sum = 0.0
                vec = input_vectors[time_idx]
                if vec[bit_idx1] and vec[bit_idx2]:
                    temp_sum = temp_sum + 1
                print temp_sum
            scin_total = scin_total + (temp_sum / float(len(input_vectors)))
    SCin = scin_total / (0.5 * num_inputs * (num_inputs-1))
    
    print input_vectors
    print output_vectors
    print (Pin, Din, SCin, Dout)
compute_statistics('../c17_training_vectors/003', '../c17_training_vectors/003_out')
