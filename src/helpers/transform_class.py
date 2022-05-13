
import numpy as np


class Moments():
    def __init__(self, left_orthon_matrix, right_orthon_matrix):
        self.l_orthon_matrix = left_orthon_matrix
        self.r_orthon_matrix = right_orthon_matrix

    def direct_moments(self, A):
        return np.dot(self.l_orthon_matrix.T, np.dot(A, self.r_orthon_matrix))

    def inverse_moments(self, A):
        matrix = np.dot(self.l_orthon_matrix, np.dot(A, self.r_orthon_matrix.T))
        # Fix overflow and underflow problem
        for i in range(8):
            for j in range(8):
                if (matrix[i, j] - int(matrix[i, j])) < 0.5:
                    matrix[i, j] = int(matrix[i, j])
                else:
                    matrix[i, j] = int(matrix[i, j]) + 1
                if matrix[i, j] > 255:
                    matrix[i, j] = 255.0
                elif matrix[i, j] < 0:
                    matrix[i, j] = 0.0
        return matrix
