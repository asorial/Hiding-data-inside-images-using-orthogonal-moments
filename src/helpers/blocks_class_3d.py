

class BlocksImageChanels():
    def __init__(self, image_array, sblock_rows=8, sblock_cols=8):
        self.image_array = image_array
        self.size_block_rows = sblock_rows
        self.size_block_cols = sblock_cols
        self.blocks_in_rows = (
            self.image_array.shape[0] // self.size_block_rows
        )
        self.blocks_in_cols = (
            self.image_array.shape[1] // self.size_block_cols
        )

    def get_image(self):
        return self.image_array

    def get_channel(self, chan):
        return self.image_array[:, :, chan]

    def max_num_blocks_channels(self):
        return self.blocks_in_rows * self.blocks_in_cols

    def image_size(self):
        return self.image_array.shape

    def get_coord_block_channels(self, num_block):
        if num_block < self.max_num_blocks_channels():
            L = []
            row_block = int(num_block / self.blocks_in_cols)
            col_block = num_block % self.blocks_in_cols
            L.append(row_block * self.size_block_rows)
            L.append((row_block + 1) * self.size_block_rows)
            L.append(col_block * self.size_block_cols)
            L.append((col_block + 1) * self.size_block_cols)
            return L
        raise Exception("There is no such block")

    def get_3d_block(self, num_block):
        try:
            pos = self.get_coord_block_channels(num_block)
            return self.image_array[pos[0]:pos[1], pos[2]:pos[3], :]
        except Exception:
            return None

    def get_block_channel(self, num_block, chan):
        try:
            pos = self.get_coord_block_channels(num_block)
            matrix = (
                self.get_channel(chan)[
                    pos[0]:pos[1],
                    pos[2]:pos[3]
                ]
            )
            if matrix.shape != (1, 1):
                return matrix
            else:
                return matrix[0][0]
        except Exception:
            return None

    def set_block_channel(self, block, num_block, chan):
        pos = self.get_coord_block_channels(num_block)
        self.get_channel(chan)[pos[0]:pos[1], pos[2]:pos[3]] = block

    def set_3d_block(self, block, num_block):
        pos = self.get_coord_block_channels(num_block)
        self.image_array[pos[0]:pos[1], pos[2]:pos[3], :] = block
