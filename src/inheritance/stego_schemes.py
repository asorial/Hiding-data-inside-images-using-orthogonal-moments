
from helpers.image_class import BlocksRGBImage
from helpers.transform_class import Moments
from helpers import progress_bar
from helpers.utils import *
from copy import deepcopy
import numpy as np


class StegoSchemes(Moments):
    """

    """

    def __init__(self, l_orth_matrix, r_orth_matrix, size_block, block_cap, qf):
        super().__init__(l_orth_matrix, r_orth_matrix)
        self.sblock = size_block
        self.block_cap = block_cap
        self.qf = qf

    def zig_zag_scan(self, block):
        return vzig_zag_scan(block)

    def rev_zig_zag_scan(self, coeffs):
        return mzig_zag_scan(coeffs)

    def quantized(self, block):
        # Applying the direct moments
        coeff_block = super().direct_moments(block)
        # Quantifying
        return quant(coeff_block, self.qf)

    def unquantized(self, block):
        # Multiply the previous matrix by the quantification matrix
        coeff_block = quantinv(block, self.qf)
        # Apply the inverse moment transform
        return super().inverse_moments(coeff_block)

    def insertion_method(self, vac, bin_msg):
        for index, elem in enumerate(bin_msg):
            sg = np.sign(vac[index])
            vac[index] = sg * replace(abs(round(vac[index])), elem)
        return vac

    def pos_generating(self, max_num):
        pass

    def modify_block_ins(self, block, bin_msg):
        pass

    def modify_block_ext(self, block):
        pass

    def insert(self, cover_array, msg):
        # Creating copy
        stego_array = deepcopy(cover_array)
        # Instance
        blocks_inst = BlocksRGBImage(stego_array, self.sblock, self.sblock)
        # Max number of blocks
        max_num_blocks = blocks_inst.max_num_blocks_image()
        # Partitioning the message
        part_msg = parti_bin_msg(msg, self.block_cap)
        # Generation positions
        positions = self.pos_generating(max_num_blocks)
        print("-------------------------------------------------------------" +
            "-----------------")
        print("Embedding secrete bits:")
        print("-------------------------------------------------------------" +
            "-----------------")
        # Initial call to print 0% progress
        progress_bar.printProgressBar(0, max_num_blocks, prefix='Progress:',
            suffix='Complete', length=50)
        for index, num_block in enumerate(positions):
            # Geting block
            block = blocks_inst.get_block_image(num_block)
            # Modifiyin block
            block = self.modify_block_ins(block, part_msg[index])
            blocks_inst.set_block_image(block, num_block)
            progress_bar.printProgressBar(index+1, max_num_blocks,
                prefix='Progress:', suffix='Complete', length=50)

        return stego_array

    def extraction_method(self, vac):
        bin_msg = ""
        for elem in vac:
            bin_msg += ext_lsb(abs(round(elem)))
        return bin_msg

    def extraction(self, stego_array):
        # Initial value
        bin_msg = ""
        # Instance
        blocks_inst = BlocksRGBImage(stego_array, self.sblock, self.sblock)
        # Max number of blocks
        max_num_blocks = blocks_inst.max_num_blocks_image()
        # Generation positions
        positions = self.pos_generating(max_num_blocks)
        print("-------------------------------------------------------------" +
            "-----------------")
        print("Extracting secrete bits:")
        print("-------------------------------------------------------------" +
            "-----------------")
        # Initial call to print 0% progress
        progress_bar.printProgressBar(0, max_num_blocks, prefix='Progress:',
            suffix='Complete', length=50)
        for index, num_block in enumerate(positions):
            # Geting block
            block = blocks_inst.get_block_image(num_block)
            # Findind de quantized coefficients
            bin_msg += self.modify_block_ext(block)
            progress_bar.printProgressBar(index+1, max_num_blocks,
                prefix='Progress:', suffix='Complete', length=50)

        return bin2char(bin_msg)
