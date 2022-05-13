# -*- coding: utf-8 -*-
from stego_schemes.stego_orthon_moments_inher import StegoOrthonMoments2020
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
    # Key
    private_key = "Aslorent7N;fpr-y7"

    # Creating matrix
    pos_matrix = [[6, 6], [6, 1], [6, 1], [7, 6]]
    poly_label = ["qK", "qKK", "qKH", "qHqK"]

    # Loading message
    file = open(os.path.join(base, 'messages/message_00.txt'), "r")
    msg = file.read()
    file.close()
    msg = increase_msg(msg, 64 ** 2 * 3 * 6)

    # Building stego images. Generating results
    for index, pos in enumerate(pos_matrix):
        for image_name in image_names:
            L = []
            # Instance
            steg = StegoOrthonMoments2020(
                orth_matrix(pos[0]),
                orth_matrix(pos[1]), 64, 64 * 6, 77,
                private_key,
                0.57, 0.28, 1, 5, -1.5, 2, 0.5, -2, 3,
            )
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
                "stego_images/ortho_moments2020/" + poly_label[index],
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
