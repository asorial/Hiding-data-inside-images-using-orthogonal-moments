
from helpers.chaotic_positions_class import BetaChaoticPositions
from helpers.blocks_class import BlocksChannelImage
from inheritance.stego_schemes import StegoSchemes
from helpers.utils import *


class StegoOrthonMoments2020(StegoSchemes):
    """
    The steganographic algorithm embeds a secrete message at the first eight
    coefficients of high frequency image. Moreover, this embedding method uses
    the Beta chaotic map to determine the order of the blocks where the secret
    bits will be inserted. In addition, from a 128-bit private key and the steps
    of a cryptography algorithm according to the Advanced Encryption Standard
    (AES) to generate the key expansion, the proposed method generates a key
    expansion of 2560 bits, with the purpose to permute the first eight
    coefficients of high frequency before the insertion. The insertion takes
    eventually place at the first eight high frequency coefficients in the
    transformed orthogonal moments domain. Before the insertion of the message
    the image undergoes a series of transformations.
    """

    def __init__(self, m1, m2, sb, bc, qf, ky, x, k, a, b1, c1, b2, c2, x0, x1):
        super().__init__(m1, m2, sb, bc, qf)
        self.x = x
        # Instance
        self.bcp = BetaChaoticPositions(k, a, b1, c1, b2, c2, x0, x1)
        # Hilbert curve scan
        self.hilbertcs = hilbert_curve_scan(list(range(64)))
        # Key expansion
        self.seqperm = aes_binary_seq(ky)
        self.emb_size = bc // sb
        self.part_perm = parti_bin_msg(
            increase_msg(self.seqperm, 64 ** 2 * 3 * self.emb_size),
            self.emb_size
        )
        # Dividing into block sequences of 8 bits
        self.n = len(self.seqperm) // 8
        self.index = -1

    def pos_generating(self, max_num):
        return self.bcp.chaotic_positions(self.x, list(range(max_num)))

    def modify_block_ins(self, block, bin_msg):
        # Initial values
        part_msg = parti_bin_msg(bin_msg, self.emb_size)
        # Instance
        blocks_8x8_inst = BlocksChannelImage(block)
        for index_msg, elem in enumerate(self.hilbertcs):
            block_8x8 = blocks_8x8_inst.get_block(elem)
            # Findind de quantized coefficients
            vac = super().zig_zag_scan(super().quantized(block_8x8))
            self.index += 1
            # Permuting
            acp = qperm(vac[1:self.emb_size + 1], self.part_perm[self.index])
            # Embedding
            acp = super().insertion_method(acp, part_msg[index_msg])
            # Rearranging elements
            vac[1:self.emb_size + 1] = invqperm(acp, self.part_perm[self.index])
            # Unquantization
            block_8x8 = super().unquantized(super().rev_zig_zag_scan(vac))
            # Updating block
            blocks_8x8_inst.set_block(block_8x8, elem)
        return block

    def modify_block_ext(self, block):
        # Initial values
        bin_msg = ""
        # Instance
        blocks_8x8_inst = BlocksChannelImage(block)
        for elem in self.hilbertcs:
            block_8x8 = blocks_8x8_inst.get_block(elem)
            # Findind de quantized coefficients
            vac = super().zig_zag_scan(super().quantized(block_8x8))
            self.index += 1
            # Permuting
            acp = qperm(vac[1:self.emb_size + 1], self.part_perm[self.index])
            # Extracting
            bin_msg += super().extraction_method(acp)
        return bin_msg
