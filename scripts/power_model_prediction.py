"""
Given a power model created from the construct_power_model.py script and a sequences
file which contains test sequences, this script will perform estimation based
on the model and will compute error statistics versus the actual power reported 
by PrimeTime.
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
        print('Usage: python power_model_prediction.py <Sequences paths file> <power model binary path>')
        sys.exit(1)

    sequences_paths_file = os.path.abspath(sys.argv[1])
    power_model_binary_path = os.path.abspath(sys.argv[2])

    power_model = None
    print('Reading power model binary (pickled) from path %s' % power_model_binary_path)
    with open(power_model_binary_path, 'rb') as f:
        power_model = pickle.load(f)
        
    print('Successfully read power model binary into memory')

    print('Reading sequences paths file from file %s' % sequences_paths_file)
    sequence_paths = []
    with open(sequences_paths_file, 'r') as f:
        for sequence_path in f:
            sequence_paths.append(sequence_path.strip())

    print('Successfully read sequence paths into memory')

    actual_power = []
    seq_statistics = []
    for sequence in sequence_paths:
        power = util.compute_power('%s_pt_power' % sequence)
        actual_power.append(power)
        statistics = util.compute_statistics(sequence, '%s_out' %sequence)
        seq_statistics.append(statistics)
    
    prediction = util.compute_power_estimate(power_model, seq_statistics)
    errors = [] 
    for idx in range(0, len(prediction)):
        pt_power = actual_power[idx]
        pred_power = prediction[idx]
        error = (pt_power - pred_power) / pt_power
        errors.append(error)
        print('seq: %03d, actual: %.10f, predicted: %.10f, error: %.4f' % (idx, pt_power, pred_power, error))
    sys.exit(0)
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
