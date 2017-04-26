"""
Given data gathered from the gather_power_data.py script, which includes the
input sequences, output sequences, and power calculated by PrimeTime, this program
will construct a power model, calculate its statistics, and export it.
"""
import sys
from bitarray import bitarray
import matplotlib.pyplot as plt

def main():
    # Parse command line arguments
    if (len(sys.argv) != 3):
        print('Usage: python construct_power_model.py <Sequences paths file> <output directory>')
        sys.exit(1)

    sequences_paths_file = sys.argv[1]
    output_directory = sys.argv[2]

    sequence_paths = []
    with open(sequences_paths_file, 'r') as f:
        for sequence_path in f:
            sequence_paths.append(sequence_path.strip())

    power_model = {}
    for sequence in sequence_paths:
        power = compute_power('%s_pt_power' % sequence)
        power = None
        statistics = compute_statistics(sequence, '%s_out' % sequence)
        if statistics in power_model:
            print 'special case'
            power_model[statistics].append(power)
        else:
            power_model[statistics] = [power]
    
    # Compute histograms for every model statistic
    Pin = []
    Din = []
    SCin = []
    Dout = []
    for entry in power_model:
        Pin.append(entry[0])
        Din.append(entry[1])
        SCin.append(entry[2])
        Dout.append(entry[3])

    fig = plt.figure()
    plt.subplot(2,2,1)
    plt.hist(Pin)
    plt.title('Pin')

    plt.subplot(2,2,2)
    plt.hist(Din)
    plt.title('Din')
    
    plt.subplot(2,2,3)
    plt.hist(SCin)
    plt.title('SCin')
   
    plt.subplot(2,2,4)
    plt.hist(Dout)
    plt.title('Dout')
    plt.savefig('Power_Model_Hists.png')
    print power_model

def compute_power(input_pt_file):
    contents = []
    with open(input_pt_file, 'r') as f:
        contents = f.readlines()
    power_string = [x.strip() for x in contents[-2].split(' ')]
    power_string = [x for x in power_string if x != ''] 
    power_string = power_string[1:5]
    power_string = [float(x) for x in power_string]
    return tuple(power_string)

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
            temp_sum = 0.0
            for time_idx in range(0, len(input_vectors)):
                vec = input_vectors[time_idx]
                if (vec[bit_idx1] == True) and (vec[bit_idx2] == True):
                    temp_sum = temp_sum + 1
            scin_total = scin_total + (float(temp_sum) / float(len(input_vectors)))
    SCin = scin_total * (2.0 / (num_inputs * (num_inputs-1)))
    
    return (Pin, Din, SCin, Dout)

if __name__ == "__main__":
    main()
