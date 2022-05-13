

import matplotlib.pyplot as plt
from helpers.utils import *
import matplotlib as mpl
import numpy as np
import os


def main():

    # Directory
    base = "src/static"
    base = os.path.join(os.getcwd(), base)
    dir_datas = os.path.join(base, "results/Data_Set_I")
    if not os.path.exists(dir_datas):
        os.makedirs(dir_datas)

    method_name, size_data = "Data_Set_I", 100
    # method_name, size_data = "Data_Set_II", 100
    # method_name, size_data = "Data_Set_III", 17
    # method_name, size_data = "Data_Set_IV", 17

    # PSNR
    # j = 0
    # metr = "PSNR"
    # UIQI
    j = 1
    metr = "UIQI"
    # IF
    # j = 2
    # metr = "IF"
    # RE
    # j = 3
    # metr = "RE"

    L = [
        1, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 29, 31, 39, 41,
        49, 51, 59, 61, 69, 71, 79, 81, 89, 90, 91, 92, 93, 94, 95, 96, 97,
        98]

    data_to_plot = []

    files_names = ['0.dat', '1.dat', '2.dat', '3.dat', '4.dat', '5.dat']

    for data_name in files_names[:-1]:
        dir_dat_file = os.path.join(
        dir_datas,
        data_name
        )
        signal = np.loadtxt(dir_dat_file)
        data_to_plot.append(list(signal[:, j].T))

    dir_dat_file = os.path.join(
    dir_datas,
    files_names[-1]
    )
    signal = np.loadtxt(dir_dat_file)
    # matrix = np.array(signal[:, j]).reshape(size_data, size_data).T
    matrix = vector2matrix(signal[:, j], size_data).T

    aux_matrix = plot_matrix(matrix, L)

    n = len(L)
    for i in range(n):
        data_to_plot.append(list(aux_matrix[:, i].T))

    matrix_plot = np.array(data_to_plot).T
    # Create a figure instance
    fig = plt.figure(1, figsize=(7, 7))
    # fig = plt.figure(1, figsize=(18, 7))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(matrix_plot, notch=0, sym='r+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='blue')
    plt.setp(bp['whiskers'], color='blue', linestyle='--')
    plt.setp(bp['medians'], color='red')
    plt.setp(bp['fliers'], color='red')
    # plt.grid(True)

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax.yaxis.grid(
        True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    # Custom x-axis labels
    pol_method_name = []
    pol_method_name.append("Sah. M.")
    pol_method_name.append("Said. M.")
    pol_method_name.append("Chow. M.")
    pol_method_name.append("Hem. M.")
    pol_method_name.append("Tauh. M.")
    pol_method_name.extend(methods_name_sba(L))
    ax.set_xticklabels(pol_method_name, rotation=-90)

    ax.set_ylabel(metr + " Values")

    # Creating dir of *.eps file
    direps = os.path.join(base, "plots")
    if not os.path.exists(direps):
        os.makedirs(direps)
    direps = os.path.join(
        direps,
        method_name + "_" + metr
    )
    # direps += ".jpg"
    direps += ".eps"
    # Save the figure
    fig.savefig(direps, bbox_inches='tight')
    # fig.savefig('HScan.eps', bbox_inches='tight')


if __name__ == '__main__':
    main()
