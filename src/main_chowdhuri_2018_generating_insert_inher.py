# -*- coding: utf-8 -*-
from stego_schemes.stego_chowdhuri_inher_2018 import Chowdhuri2018
from helpers.orthonornal_matrix import orth_matrix
from helpers.utils import char2bin, increase_msg
import imageio
import os


def main():
    # Directory
    base = "src/static"
    base = os.path.join(os.getcwd(), base)
    dir_covers = os.path.join(base, "cover_images")
    if not os.path.exists(dir_covers):
        os.makedirs(dir_covers)
    # Cover arrays
    image_names = os.listdir(dir_covers)

    # Loading message
    file = open(os.path.join(base, 'messages/message_00.txt'), "r")
    msg = file.read()
    file.close()
    msg = increase_msg(msg, 64 ** 2 * 3 * 4)

    # Building stego images. Generating results
    for image_name in image_names:
        steg = Chowdhuri2018(
            orth_matrix(10),
            orth_matrix(10), 8, 4, 77,
            "Aslorent7N;fpr-y7"
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
            "stego_images/chowdhuri2018",
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


if __name__ == '__main__':
    main()