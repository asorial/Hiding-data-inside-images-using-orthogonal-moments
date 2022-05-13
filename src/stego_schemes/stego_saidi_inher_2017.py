
from inheritance.stego_schemes import StegoSchemes
from helpers.utils import *


class StegoSaidi2017(StegoSchemes):
    """
    In this paper, a novel steganographic scheme is proposed based on chaotic
    map in the DCT domain. The proposed method apply the DCT on the cover image,
    scan the AC coefficients in a zigzag form from the least significant to the
    most significant one, this scan will lead us eventually to precise the
    embedding positions through a chaotic function as well as the maximum
    allowed payload relative to a computed SSIM threshold. A quantitative study
    shows the check of the designed method to the requirement of
    imperceptibility and flexibility.
    """

    def __init__(self, l_orth_m, r_orth_m, s_block, b_cap, qf, x0, p, delta):
        super().__init__(l_orth_m, r_orth_m, s_block, b_cap, qf)
        self.N = b_cap
        self.delta = delta
        # Chaotic positions
        self.pos = random_list(x0, p, list(range(self.N)))

    def pos_generating(self, max_num):
        return list(range(max_num))

    def __process_block__(self, block, positive=True):
        # Applying the direct moments
        coeffs = super().direct_moments(block)
        # Applying the zig_zag scan
        zcoeffs = super().zig_zag_scan(coeffs)
        # Deleting the last N elements
        coeffs_seq = zcoeffs[:-self.N]
        # Reset a specific number N of AC coefficients to 0 in the block
        coeffs_seq.extend([0.0 for i in range(self.N)])
        # Apply the IDCT on each modified block
        matrix = super().rev_zig_zag_scan(coeffs_seq)
        block_8x8 = super().inverse_moments(matrix)
        # Apply the DCT on each previous block
        coeffs_block = super().direct_moments(block_8x8)
        # Applying the zig_zag scan
        zcoeffs_block = super().zig_zag_scan(coeffs_block)
        if positive:
            return (
                zcoeffs_block,
                sum(abs(np.array(zcoeffs_block))) * self.delta / 100,
            )
        else:
            return (
                zcoeffs_block[-self.N:],
                sum(abs(np.array(zcoeffs_block))) * self.delta / 100,
                zcoeffs[-self.N:]
            )

    def __insert__(self, vac, bin_msg, Delta):
        for index, elem in enumerate(bin_msg):
            if elem == "0":
                vac[self.pos[index]] = vac[self.pos[index]] - Delta
            else:
                vac[self.pos[index]] = vac[self.pos[index]] + Delta
        return vac

    def modify_block_ins(self, block, bin_msg):
        pro = self.__process_block__(block)
        pro[0][-self.N:] = self.__insert__(
            pro[0][-self.N:],
            bin_msg,
            pro[1],
        )
        return super().inverse_moments(super().rev_zig_zag_scan(pro[0]))

    def modify_block_ext(self, block):
        pass
