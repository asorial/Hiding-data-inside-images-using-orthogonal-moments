
from inheritance.stego_schemes import StegoSchemes


class StegoSahar2016(StegoSchemes):
    """
    The secret bits are embedded in LSBs of the middle frequency coefficients.
    """

    def __init__(self, l_orth_matrix, r_orth_matrix, s_block, b_cap, qf):
        super().__init__(l_orth_matrix, r_orth_matrix, s_block, b_cap, qf)
        self.b_cap = b_cap

    def pos_generating(self, max_num):
        return list(range(max_num))

    def modify_block_ins(self, block, bin_msg):
        # Findind de quantized coefficients
        vac = super().zig_zag_scan(super().quantized(block))
        part_vac = vac[9:self.b_cap + 9]
        part_vac = super().insertion_method(part_vac, bin_msg)
        vac[9:self.b_cap + 9] = part_vac
        return super().unquantized(super().rev_zig_zag_scan(vac))

    def modify_block_ext(self, block):
        # Findind de quantized coefficients
        vac = super().zig_zag_scan(super().quantized(block))
        return super().extraction_method(vac[9:self.b_cap + 9])
