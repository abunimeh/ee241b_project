"""
Given data gathered from the gather_power_data.py script, which includes the
input sequences, output sequences, and power calculated by PrimeTime, this program
will construct a power model, calculate its statistics, and export it.
"""
import sys
from bitarray import bitarray
import matplotlib.pyplot as plt
import os
import cPickle as pickle
import numpy as np
import util

def construct_4d_table(sequence_paths):
    print('Computing 4D table power model')
    power_model = {}
    for sequence in sequence_paths:
        power = util.compute_power('%s_pt_power' % sequence)
        statistics = util.compute_statistics(sequence, '%s_out' % sequence)
        if statistics in power_model:
            print 'special case - multiple power numbers for same 4D tuple'
            power_model[statistics].append(power)
        else:
            power_model[statistics] = [power]

    # Take average of all power numbers that share a common tuple
    final_power_model = {}
    for stat_tuple, power_list in power_model.iteritems():
        final_power_model[stat_tuple] = np.mean(power_list)
    return power_model

def construct_linear_model(sequence_paths):
    print('Computing linear power model based on overall Pin, Din, SCin, Dout')
    A = np.zeros((len(sequence_paths), 5))
    b = np.zeros((len(sequence_paths), 1))
    for idx in range(0, len(sequence_paths)):
        power = util.compute_power('%s_pt_power' % sequence_paths[idx])
        statistics = util.compute_statistics(sequence_paths[idx], '%s_out' % sequence_paths[idx])
        A[idx] = [1, statistics[0], statistics[1], statistics[2], statistics[3]]
        b[idx] = power
    power_model = np.linalg.lstsq(A, b)[0]
    print('Computed these coefficients using least squares')
    print(power_model)
    return power_model

def save_statistics_histogram(sequence_paths, histogram_output_path):
    # Compute histograms for every model statistic
    Pin = []
    Din = []
    SCin = []
    Dout = []
    for sequence in sequence_paths:
        statistics = util.compute_statistics(sequence, '%s_out' % sequence)
        Pin.append(statistics[0])
        Din.append(statistics[1])
        SCin.append(statistics[2])
        Dout.append(statistics[3])

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
    print('Saving 4D tuple distribution histogram to %s' % histogram_output_path)
    plt.savefig(histogram_output_path)

def main():
    # Parse command line arguments
    if (len(sys.argv) != 5):
        print('Usage: python construct_power_model.py <Sequences paths file> <model type = 4d_table/linear/quadratic/cubic/full_linear> <output directory> <output model binary filename>')
        sys.exit(1)

    sequences_paths_file = os.path.abspath(sys.argv[1])
    model_type = sys.argv[2]
    output_directory = os.path.abspath(sys.argv[3])
    output_model_filename = sys.argv[4]

    output_model_path = '%s/%s' % (output_directory, output_model_filename)

    print('Cleaning or creating output directory: %s' % output_directory)
    # Create output directory and clean the output artifacts if they already exist
    if os.path.isdir(output_directory):
        if os.path.isfile(output_model_path):
            os.remove(output_model_path)
    else:
        os.mkdir(output_directory)

    print('Getting sequence paths from file %s' % sequences_paths_file)
    sequence_paths = []
    with open(sequences_paths_file, 'r') as f:
        for sequence_path in f:
            sequence_paths.append(sequence_path.strip())

    print('Using model type: %s' % model_type)
    power_model = None
    if model_type == '4d_table':
        power_model = construct_4d_table(sequence_paths)
    elif model_type == 'linear':
        power_model = construct_linear_model(sequence_paths)
    elif model_type == 'quadratic':
        power_model = construct_quadratic_model(sequence_paths)
    elif model_type == 'cubic':
        power_model = construct_cubic_model(sequence_paths)
    else:
        print('Provide a valid power model type')
        sys.exit(1)

    # Save power model as binary to be unpacked by the estimation script
    print('Saving power model to location: %s' % output_model_path)
    with open(output_model_path, 'wb') as f:
        pickle.dump(power_model, f, pickle.HIGHEST_PROTOCOL)

    save_statistics_histogram(sequence_paths, '%s/stats_histogram.png' % output_directory) 

if __name__ == "__main__":
    main()
