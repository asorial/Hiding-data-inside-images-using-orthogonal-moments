
from inheritance.stego_schemes import StegoSchemes
from helpers.utils import *
import numpy as np


class Hemalatha2019(StegoSchemes):
    """
    Steganography deal with hiding information science, which offers an ultimate
    security in defence, profitable usages, thus sending the imperceptible
    information, will not be bare or distinguished by others. The aim of this
    paper is to propose a novel steganographic method in JPEG images to highly
    enrich a data security by RSA algorithm and attains higher payload by
    modified quantisation table. The goals of this paper are to be recognised
    through: 1) modify the quantisation table of the JPEG-JSTEG tool, hiding
    secret message with its middle frequency to offer great embedding capacity;
    2) for challenge, secure RSA algorithm is used to prevent data from
    extraction. A broad experimental evaluation compares the performance of our
    proposed work with existing JSTEG was conducted.
    """

    def __init__(self, l_orth_matrix, r_orth_matrix, s_block, b_cap, qf):
        super().__init__(l_orth_matrix, r_orth_matrix, s_block, b_cap, qf)
        self.qf = qf
        self.ind = pos_middle()[:b_cap // 2]

    def pos_generating(self, max_num):
        return list(range(max_num))

    def __quantized_coeffs__(self, block):
        # Applying the direct moments
        coeff_block = super().direct_moments(block)
        # Quantifying and applying the zig_zag scan
        return super().zig_zag_scan(quantm(coeff_block, self.qf).round())

    def __unquantized_coeffs__(self, vcoeff):
        # Multiply the previous matrix by the quantification matrix
        coeff_block = quantminv(super().rev_zig_zag_scan(vcoeff), self.qf)
        # Apply the inverse moment transform
        return super().inverse_moments(coeff_block)

    def __insert__(self, byte, bin_msg):
        nbyte = np.sign(byte) * replace_l2sb(abs(round(byte)), bin_msg)[0]
        return nbyte

    def modify_block_ins(self, block, bin_msg):
        # Initial values
        index = -1
        part_msg = parti_bin_msg(bin_msg, 2)
        vac = self.__quantized_coeffs__(block)
        for pos_midd in self.ind:
            index += 1
            vac[pos_midd] = self.__insert__(vac[pos_midd], part_msg[index])
        return self.__unquantized_coeffs__(vac)

    def modify_block_ext(self, block):
        pass
