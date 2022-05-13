
import math
import hashlib
import numpy as np


def num2bin(n, width=8):
    return np.binary_repr(n, width)


def __bin2dec(bin_seq):
    dec_repr = 0
    n = len(bin_seq)
    for i in range(n):
        if bin_seq[n - i - 1] != '0':
            dec_repr += 2 ** i
    return dec_repr


def bin2dec(data):
    return [__bin2dec(data[i:i+8]) for i in range(0, len(data), 8)]


def char2bin(data):
    return "".join(format(ord(x), '08b') for x in data)


def dec2bin(data):
    return "".join(format(x, '08b') for x in data)


def dec2char(data):
    return "".join(chr(x) for x in data)


def bin2char(bin_seq):
    return ''.join(
        (chr(int(bin_seq[i:i+8], 2)) for i in range(0, len(bin_seq), 8))
    )


def char2dec(data):
    return [ord(x) for x in data]


def bitxor(bit_1, bit_2):
    if bit_1 == bit_2:
        return "0"
    else:
        return "1"


def lsb(byte):
    if byte % 2 == 0:
        return "0"
    else:
        return "1"


def pwlcm(x, p):
    if x >= 0 and x < p:
        return x / p
    elif x >= p and x < 0.5:
        return (x - p) / (0.5 - p)
    elif x >= 0.5 and x < 1:
        return pwlcm(1 - x, p)


def chaotic_map(x, p, n):
    L = []
    for i in range(n):
        x = pwlcm(x, p)
        L.append(int(math.floor(x * 10 ** (14) % n)))
    return L


def perm(L, ind):
    pos = []
    n = len(ind)
    for i in range(n):
        pos.append(L[ind[i]])
    return pos


def set_diff(L1, L2):
    n = len(L2)
    for i in range(n):
        L1.remove(L2[i])
    return L1


def list_reduced(L):
    R = []
    for i in L:
        if i not in R:
            R.append(i)
    return R


def random_list(x, p, L):
    pos = []
    ind = []
    ind = list_reduced(chaotic_map(x, p, len(L)))
    pos = perm(L, ind)
    if len(pos) == len(L):
        return pos
    elif len(pos) == 1:
        return L
    else:
        return pos + random_list(x, p, set_diff(L, pos))
    return pos


def replace(byte_init, bit):
    if bit == '0':
        if byte_init % 2 == 0:
            byte_fin = byte_init
        else:
            byte_fin = byte_init - 1
    elif bit == '1':
        if byte_init % 2 == 0:
            byte_fin = byte_init + 1
        else:
            byte_fin = byte_init
    return byte_fin


def ext_lsb(byte):
    if byte % 2 == 0:
        return '0'
    return '1'


def replace_l2sb(byte_init, listbit):
    bin_cad = num2bin(int(byte_init))
    return bin2dec(bin_cad[:-2] + listbit)


def ext_l2sb(byte_init):
    return num2bin(byte_init)[-2:]


def or_operation(x, y):
    if len(x) != len(y):
        raise ValueError("It is not possible to perform this operation")
    n = len(x)
    return "".join(("0" if x[i] == y[i] else "1") for i in range(n))


def or_oper(x, y):
    return bin2dec(or_operation(dec2bin(x), dec2bin(y)))


def increase(key, n):
    seq = blake2b_bin(key)
    while len(seq) < n:
        seq += blake2b_bin(seq[-128:])
    return seq[:n]

def increase_msg(msg, n):
    seq = msg
    while len(seq) < n:
        seq += msg
    return seq[:n]


def sbox():
    matrix = np.array([
        [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171,
            118],
        [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164,
            114, 192],
        [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49,
            21],
        [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
        [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
        [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
        [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159,
            168],
        [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243,
            210],
        [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25,
            115],
        [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11,
            219],
        [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
        [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122,
            174, 8],
        [186, 120,  37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139,
            138],
        [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
        [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40,
            223],
        [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187,
            22]])
    return matrix


def rotword(row):
    L = row[1:]
    L.append(row[0])
    return L

def rcon(col):
    matrix = np.array([
        [1, 2, 4, 8, 16, 32, 64, 128, 27, 54],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    return list(matrix[:, col])

def sub_bytes(v):
    L = []
    A = sbox()
    n = len(v)
    for i in range(n):
        if len(hex(v[i])[2:]) != 1:
            aux = A[int(hex(v[i])[2:][0], 16)][int(hex(v[i])[2:][1], 16)]
            L.append(aux)
        else:
            L.append(A[0][int(hex(v[i])[2:], 16)])
    return L

def sub_keys_aes(key):
    L = []
    w = []
    deckey = char2dec(key)
    for j in range(4):
        w.append([deckey[4 * j] + k for k in range(4)])
    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = or_oper(
                sub_bytes(
                    rotword(temp)),
                    rcon(i // 4 - 1)
                )
        w.append(or_oper(w[i - 4], temp))
    return list(np.array(w).reshape(-1))


def aes_binary_seq(key):
    L = sub_keys_aes(key)[16:]
    L.extend(sub_keys_aes(dec2char(L[-16:]))[16:])
    return dec2bin(L)


def hilbert_curve():
    A = np.array([
        [0,  8,  9,  1,  2,  3, 11, 10],
        [18, 19, 27, 26, 25, 17, 16, 24],
        [32, 33, 41, 40, 48, 56, 57, 49],
        [50, 58, 59, 51, 43, 42, 34, 35],
        [36, 37, 45, 44, 52, 60, 61, 53],
        [54, 62, 63, 55, 47, 46, 38, 39],
        [31, 23, 22, 30, 29, 28, 20, 21],
        [13, 12,  4,  5,  6, 14, 15,  7]])
    return A.reshape(-1)


def hilbert_curve_scan(seq):
    L = []
    postions = hilbert_curve()
    for pos in postions:
        L.append(seq[pos])
    return L


def qperm(vac, seqbin):
    L = []
    for i in range(len(seqbin)):
        if seqbin[i] == '1':
            L.append(vac[i])
    if len(L) != len(seqbin):
        for i in range(len(seqbin)):
            if seqbin[i] == '0':
                L.append(vac[i])
    return L


def invqperm(vac, seqbin):
    L = list(range(len(seqbin)))
    j = -1
    aux = vac[0:seqbin.count("1")]
    for i in range(len(seqbin)):
        if seqbin[i] == '1':
            j += 1
            L[i] = aux[j]
    j = -1
    aux = vac[seqbin.count("1"):]
    for i in range(len(seqbin)):
        if seqbin[i] == '0':
            j += 1
            L[i] = aux[j]
    return L


def matrix_zig_zag():
    A = np.array([
        [0,    1,     8,    16,     9,     2,     3,    10],
        [17,    24,    32,    25,    18,    11,     4,     5],
        [12,    19,    26,    33,    40,    48,    41,    34],
        [27,    20,    13,     6,     7,    14,    21,    28],
        [35,    42,    49,    56,    57,    50,    43,    36],
        [29,    22,    15,    23,    30,    37,    44,    51],
        [58,    59,    52,    45,    38,    31,    39,    46],
        [53,    60,    61,    54,    47,    55,    62,    63]])
    return A


def vzig_zag_scan(A):
    L = []
    permutation = matrix_zig_zag().reshape(-1)
    seq = A.reshape(-1)
    for pos in permutation:
        L.append(seq[pos])
    return L


def inv_vzig_zag_scan(A):
    return vzig_zag_scan(A.T)


def mzig_zag_scan(vect):
    L = list(np.zeros(len(vect)))
    positions = list(matrix_zig_zag().reshape(-1))
    for index, pos in enumerate(positions):
        L[pos] = vect[index]
    return np.array(L).reshape(8, 8)


def quantm(A, QF):
    if QF > 50:
        F = (100 - QF) / 50
    else:
        F = 50 / QF
    Q = np.array([
        [16, 11, 10, 16, 1, 1, 1, 1],
        [12, 12, 14, 1, 1, 1, 1, 55],
        [14, 13, 1, 1, 1, 1, 69, 56],
        [14, 1, 1, 1, 1, 87, 80, 62],
        [1, 1, 1, 1, 68, 109, 103, 77],
        [1, 1, 1, 64, 81, 104, 113, 92],
        [1, 1, 78, 87, 103, 121, 120, 101],
        [1, 92, 95, 98, 112, 100, 103, 99]])
    Q = Q * F
    quant_matrix = [i / j for i, j in zip(A.reshape(-1), Q.reshape(-1))]
    return np.array(quant_matrix).reshape(8, 8)


def quantminv(A, QF):
    if QF > 50:
        F = (100 - QF) / 50
    else:
        F = 50 / QF
    Q = np.array([
        [16, 11, 10, 16, 1, 1, 1, 1],
        [12, 12, 14, 1, 1, 1, 1, 55],
        [14, 13, 1, 1, 1, 1, 69, 56],
        [14, 1, 1, 1, 1, 87, 80, 62],
        [1, 1, 1, 1, 68, 109, 103, 77],
        [1, 1, 1, 64, 81, 104, 113, 92],
        [1, 1, 78, 87, 103, 121, 120, 101],
        [1, 92, 95, 98, 112, 100, 103, 99]])
    Q = Q * F
    quant_matrix = [i * j for i, j in zip(A.reshape(-1), Q.reshape(-1))]
    return np.array(quant_matrix).reshape(8, 8)


def pos_middle():
    Q = np.array([
        [16, 11, 10, 16, 1, 1, 1, 1],
        [12, 12, 14, 1, 1, 1, 1, 55],
        [14, 13, 1, 1, 1, 1, 69, 56],
        [14, 1, 1, 1, 1, 87, 80, 62],
        [1, 1, 1, 1, 68, 109, 103, 77],
        [1, 1, 1, 64, 81, 104, 113, 92],
        [1, 1, 78, 87, 103, 121, 120, 101],
        [1, 92, 95, 98, 112, 100, 103, 99]])
    L = vzig_zag_scan(Q.reshape(-1))
    return [pos for pos, elem in enumerate(L) if elem == 1]


def quant(A, QF):
    if QF > 50:
        F = (100 - QF) / 50
    else:
        F = 50 / QF
    Q = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]])
    Q = Q * F
    quant_matrix = [i / j for i, j in zip(A.reshape(-1), Q.reshape(-1))]
    return np.array(quant_matrix).reshape(8, 8)


def quantinv(A, QF):
    if QF > 50:
        F = (100 - QF) / 50
    else:
        F = 50 / QF
    Q = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]])
    Q = Q * F
    quant_matrix = [i * j for i, j in zip(A.reshape(-1), Q.reshape(-1))]
    return np.array(quant_matrix).reshape(8, 8)


def parti_bin_msg(bin_msg, m=8):
    n = len(bin_msg) // m
    return [bin_msg[i * m:(i + 1) * m] for i in range(n)]


def sha512bin(key):
    hexa_data = hashlib.sha512(key.encode('utf-8')).hexdigest()
    return "".join(format(ord(x), '08b') for x in hexa_data)[:512]


def elemprod(x, y):
    return [vx * vy for vx, vy in zip(x, y)]


def methods_name_sba(L):
    k = -1
    List_cad_res = []
    List_cad = ["K", "T", "H", "C", "M", "qK", "qH", "qC", "qM", "DCT"]
    for i in range(10):
        for j in range(10):
            k += 1
            if k in L:
                if i != j:
                    List_cad_res.append(List_cad[i] + List_cad[j])
                else:
                    List_cad_res.append(List_cad[i])
    return List_cad_res


def plot_matrix(A, L):
    k = -1
    dims_A = A.shape
    dims = (dims_A[0], len(L))
    matrix = np.zeros(dims)
    for j in range(dims_A[1]):
        if j in L:
            k += 1
            matrix[:, k] = A[:, j]
    return matrix


def vector2matrix(vect, n):
    m = len(vect) // n
    dims = (m, n)
    M = np.zeros(dims)
    for i in range(m):
        j = i * n
        k = (i + 1) * n
        M[i][:] = vect[j:k]
    return M
