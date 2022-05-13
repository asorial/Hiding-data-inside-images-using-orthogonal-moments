
from inheritance.stego_schemes import StegoSchemes
from helpers.utils import *


class Chowdhuri2018(StegoSchemes):
    """
    Due to the rapid growth of internet technology and the advent of various
    image processing tools, people started using digital media for hidden
    communication to protect valuable information which is important for
    multimedia commercials, health-care, medical and defense applications. On
    the other hand, image authentication and tamper detection are essential,
    especially when it is utilized for evidence of legal action. In this paper,
    a weighted matrix based steganographic scheme has been designed for highly
    compressed (Quality Factor (QF) 40) color image through discrete cosine
    transform (DCT) to maintain a good balance between payload and impercep-
    tibility. Here, the AC components are collected from (8 × 8) quantized DCT
    coefficient matrices of YCbCr channel. Then, a series of (3 × 3) original
    matrices are formed to hide secret data. The collection of AC components
    is controlled by 128 bits shared secret key. A predetermined weighted
    matrix is employedto select the embedding position within a (3 × 3)
    coefficient matrix of a cover image through the sum of the entry-wise
    multiplication operation.
    """

    def __init__(self, l_orth_m, r_orth_m, s_block, b_cap, qf, key):
        super().__init__(l_orth_m, r_orth_m, s_block, b_cap, qf)
        # Key expansion
        self.keybin = increase_msg(sha512bin(key), 64 ** 2 * 3)
        # Weighted matrix
        self.weighted_matrix = [1, 2, 3, 4, 5, 6, 7, 8, 5]
        # index
        self.index = -1

    def pos_generating(self, max_num):
        return list(range(max_num))

    def __insert__(self, vacp, bin_msg):
        mod_total = sum(elemprod(self.weighted_matrix, vacp)) % 16
        diff = bin2dec(bin_msg)[0] - mod_total
        if diff > 8:
            diff = 16 - diff
            sng = -1
        elif diff > 0:
            sng = 1
        elif diff < -8:
            diff += 16
            sng = 1
        elif diff < 0:
            sng = -1
        pos = abs(diff)
        if diff != 0:
            vacp[int(pos)] += sng
        return vacp

    def __inv_vzig_zag_scan__(self, A):
        return super().zig_zag_scan(A.T)

    def modify_block_ins(self, block, bin_msg):
        self.index += 1
        quant_block = super().quantized(block).round()
        if self.keybin[self.index] == "0":
            vac = super().zig_zag_scan(quant_block)
        else:
            vac = self.__inv_vzig_zag_scan__(quant_block)
        vac[1:10] = self.__insert__(vac[1:10], bin_msg)
        if self.keybin[self.index] == "0":
            matrix = super().rev_zig_zag_scan(vac)
        else:
            matrix = super().rev_zig_zag_scan(vac).T
        return super().unquantized(matrix)

    def modify_block_ext(self, block):
        pass
