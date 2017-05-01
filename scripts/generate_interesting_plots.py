"""
This script is all custom, takes no arguments.
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import os
import util
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import cPickle as pickle
import matplotlib.cm as cmx

def scatter3d(x,y,z, cs, colorsMap='jet', showplot=False):
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, c=scalarMap.to_rgba(cs))
    scalarMap.set_array(cs)
    fig.colorbar(scalarMap)
    if showplot: plt.show()
    return ax

def main():
    power_model_binary_path = os.path.abspath('../models/c7552_power_model/4d_table_power_model')
    power_model = None
    print('Reading power model binary (pickled) from path %s' % power_model_binary_path)
    with open(power_model_binary_path, 'rb') as f:
        power_model = pickle.load(f)

    Pin = []
    Din = []
    SCin = []
    Dout = []
    power = []
    for statistics, power_val in power_model.iteritems():
        Pin.append(statistics[0])
        Din.append(statistics[1])
        SCin.append(statistics[2])
        Dout.append(statistics[3])
        power.append(power_val * 1e6)

    ax = scatter3d(Pin, Din, power, power, showplot=False)
    ax.set_xlabel('Pin')
    ax.set_ylabel('Din')
    ax.set_zlabel('Power (uW)')
    plt.savefig('3d_plot.pdf')

if __name__ == "__main__":
    main()
