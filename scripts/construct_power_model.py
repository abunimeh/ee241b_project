"""
Given data gathered from the gather_power_data.py script, which includes the
input sequences, output sequences, and power calculated by PrimeTime, this program
will construct a power model, calculate its statistics, and export it.
"""
import sys
from bitarray import bitarray
import matplotlib.pyplot as plt
import os
import shutil
import cPickle as pickle
import util

def main():
    # Parse command line arguments
    if (len(sys.argv) != 3):
        print('Usage: python construct_power_model.py <Sequences paths file> <output directory>')
        sys.exit(1)

    sequences_paths_file = os.path.abspath(sys.argv[1])
    output_directory = os.path.abspath(sys.argv[2])

    print('Wiping or creating output directory: %s' % output_directory)
    # Create output directory and wipe its contents if it already exists
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    sequence_paths = []
    with open(sequences_paths_file, 'r') as f:
        for sequence_path in f:
            sequence_paths.append(sequence_path.strip())

    print('Computing power model from sequences file: %s' % sequences_paths_file)
    power_model = {}
    for sequence in sequence_paths:
        power = util.compute_power('%s_pt_power' % sequence)
        statistics = util.compute_statistics(sequence, '%s_out' % sequence)
        if statistics in power_model:
            print 'special case - multiple power numbers for same 4D tuple'
            power_model[statistics] = (power_model[statistics] + power) / 2.0
        else:
            power_model[statistics] = power
   
    # Save power model as binary to be unpacked by the estimation script
    power_model_binary_path = '%s/power_model' % output_directory
    print('Saving power model to location: %s' % power_model_binary_path)
    with open(power_model_binary_path, 'wb') as f:
        pickle.dump(power_model, f, pickle.HIGHEST_PROTOCOL)

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
    histogram_output_path = '%s/Power_Model_Histogram.png' % output_directory
    print('Saving 4D tuple distribution histogram to %s' % histogram_output_path)
    plt.savefig(histogram_output_path)

if __name__ == "__main__":
    main()
