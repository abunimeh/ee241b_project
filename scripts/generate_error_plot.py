"""
This script is all custom, takes no arguments.
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import os
import util
import numpy as np

def main():
    circuits = ['c17', 'c432', 'c499', 'c880', 'c1908', 'c2670', 'c6288', 'c7552']
    models = ['4d_table', 'linear', 'quadratic', 'cubic']
    model_output_path = os.path.abspath('../models/')
    model_rms_errors = {} 
    model_sd_rms = {}
    for circuit in circuits:
        for model in models:
            error_file_path = '%s/%s_power_model/%s_error' % (model_output_path, circuit, model)
            with open(error_file_path, 'r') as f:
                errors = []
                for error_line in f:
                    error_line = error_line.split('|')
                    pt_power = float(error_line[0])
                    est_power = float(error_line[1])
                    power_error = (est_power - pt_power) / pt_power
                    errors.append(power_error * 100.0)
                min_error = np.min(errors)
                max_error = np.max(errors)
                rms_error = np.sqrt(np.mean(np.square(errors)))
                mean_error = np.mean(errors)
                sd_error = np.sqrt(np.var(errors))
                sd_rms_error = np.sqrt(np.var(np.sqrt(np.square(errors))))
                if model in model_rms_errors:
                    model_rms_errors[model].append(rms_error)
                    model_sd_rms[model].append(sd_rms_error)
                else:
                    model_rms_errors[model] = [rms_error]
                    model_sd_rms[model] = [sd_rms_error]
                print('circuit: %s model: %s rms: %02.5f %% max: %02.5f %%' % (circuit.ljust(6), model.ljust(10), rms_error, max_error))
        print('\n')

    ind = np.arange(len(circuits))
    width = 0.175

    rms_errors_4d_table= model_rms_errors['4d_table'] 
    rms_errors_linear = model_rms_errors['linear']
    rms_errors_quadratic = model_rms_errors['quadratic']
    rms_errors_cubic = model_rms_errors['cubic']
    sd_4d_table = model_sd_rms['4d_table']
    sd_linear = model_sd_rms['linear']
    sd_quadratic = model_sd_rms['quadratic']
    sd_cubic = model_sd_rms['cubic']

    matplotlib.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots()
    error_bar_params = dict(lw=0.5, capsize=1, capthick=0.5)
    rects1 = ax.bar(ind, rms_errors_4d_table, width, color='darkred', yerr=sd_4d_table, error_kw=error_bar_params)
    rects2 = ax.bar(ind + width, rms_errors_linear, width, color='orangered', yerr=sd_linear, error_kw=error_bar_params)
    rects3 = ax.bar(ind + 2*width, rms_errors_quadratic, width, color='lightsalmon', yerr=sd_quadratic, error_kw=error_bar_params)
    rects4 = ax.bar(ind + 3*width, rms_errors_cubic, width, color='peachpuff', yerr=sd_cubic, error_kw=error_bar_params)

    ax.set_ylabel('RMS Error (%)')
    ax.set_title('Accuracy of Power Models Across ISCAS 85 Benchmark Circuits')
    ax.set_xticks(ind + 1.5*width)
    ax.set_xticklabels(circuits)
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), models)
    ax.set_ylim([0,20])
    ax.set_aspect(0.2)

    ax.text(rects2[6].get_x() + rects2[6].get_width()/2.0, 15, '%.2f%%' % rms_errors_linear[6], ha='center', va='bottom')
    plt.savefig('error_plot.pdf')

if __name__ == "__main__":
    main()
