# -*- coding: utf-8 -*-
from stego_schemes.stego_tauhid_inher_2019 import StegoTauhid2019
from helpers.orthonornal_matrix import orth_matrix
from helpers.utils import char2bin, increase_msg
from helpers.stego_metrics import Metrics
import numpy as np
import imageio
import os


def main():
    # Directory
    base = "src/static"
    base = os.path.join(os.getcwd(), base)
    dir_covers = os.path.join(base, "cover_images/Data_Set_IV")
    if not os.path.exists(dir_covers):
        os.makedirs(dir_covers)
    # Cover arrays
    image_names = os.listdir(dir_covers)

    # Creating matrix
    M_Metrics = []

    # Creating directory
    dir_dat_file = os.path.join(base, "results")
    if not os.path.exists(dir_dat_file):
        os.makedirs(dir_dat_file)
    dir_dat_file = os.path.join(
        dir_dat_file,
        dir_covers[0].split("/")[-2]
    )
    dir_dat_file = "%sDataSet_IV_Tauhid2019.dat" % dir_dat_file

    # Instance
    metr = Metrics()

    # Loading message
    file = open(os.path.join(base, 'messages/message_00.txt'), "r")
    msg = file.read()
    file.close()
    msg = increase_msg(msg, 64 ** 2 * 3 * 6)

    # Building stego images. Generating results
    for image_name in image_names:
        # Instance
        steg = StegoTauhid2019(
            orth_matrix(10),
            orth_matrix(10), 8, 6, 77
        )
        L = []
        # Load cover images
        dir_image = os.path.join(
        dir_covers,
        image_name
        )
        cover_array = imageio.imread(dir_image)
        # Creating the stego images
        stego_array = steg.insert(cover_array, char2bin(msg))
        # Creating directory
        dir_save = os.path.join(
            base,
            "stego_images/tauhid2019",
        )
        if not os.path.exists(dir_save): os.makedirs(dir_save)
        dir_save = os.path.join(
            dir_save,
            dir_image.split("/")[-1][:-4],
        )
        dir_save = (
            "%s.%s" %
            (dir_save, dir_image.split(".")[1])
        )
        # Save stego image
        imageio.imsave(dir_save, stego_array)

        # Experimental analysis
        L.append(metr.psnr(cover_array, stego_array))
        L.append(metr.uiqi(cover_array, stego_array))
        L.append(metr.image_fid(cover_array, stego_array))
        L.append(metr.rel_entropy(cover_array, stego_array))
        print(" ")
        print("Experimental analysis")
        print(" ")
        print("PSNR: ", L[0])
        print(" ")
        print("UIQI: ", L[1])
        print(" ")
        print("IF: ", L[2])
        print(" ")
        print("RE: ", L[3])
        print(" ")
        # Creating cols
        M_Metrics.append(L)
        # Saving results
        np.savetxt(dir_dat_file, M_Metrics, fmt="%.9e")

    # Saving results
    np.savetxt(dir_dat_file, M_Metrics, fmt="%.9e")


if __name__ == '__main__':
    main()
