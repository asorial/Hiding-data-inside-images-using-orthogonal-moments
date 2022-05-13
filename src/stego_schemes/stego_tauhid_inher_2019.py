
from inheritance.stego_schemes import StegoSchemes
from helpers.utils import *
import numpy as np

class StegoTauhid2019(StegoSchemes):
    """
    In this paper, a secure DCT steganography method is proposed.
    """

    def __init__(self, l_orth_matrix, r_orth_matrix, s_block, b_cap, qf):
        super().__init__(l_orth_matrix, r_orth_matrix, s_block, b_cap, qf)
        self.c = b_cap

    def pos_generating(self, max_num):
        return list(range(max_num))

    def modify_block_ins(self, block, bin_msg):
        # Findind quantized coefficients
        vac = super().zig_zag_scan(super().quantized(block).round())
        vac[1:self.c + 1] = super().insertion_method(vac[1:self.c + 1], bin_msg)
        return super().unquantized(super().rev_zig_zag_scan(vac))

    def modify_block_ext(self, block):
        pass
