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

    print input_vectors
    print output_vectors
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
    print (Pin, Din, Dout)
compute_statistics('../c17_training_vectors/009', '../c17_training_vectors/003_out')
