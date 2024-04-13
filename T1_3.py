# i: Convert plaintext and key to Hexadecimal representation using ASCII table.
plaintext = "MALAYSIA"
key = "ISSOGOOD"

def string_to_hex(s):
    return ''.join(format(ord(c), '02x').upper() for c in s)

plaintext_hex = string_to_hex(plaintext)
key_hex = string_to_hex(key)
print(f"3.i = {plaintext_hex}, {key_hex}")


# ii: Convert hexadecimal representation to binary number.

# 3. ii
def hex_to_binary(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(len(hex_string)*4)

# Convert plaintext and key hex to binary.
plaintext_binary = hex_to_binary(plaintext_hex)
key_binary = hex_to_binary(key_hex)
print(f"3.ii = {plaintext_binary}, {key_binary}")


# 3. iii
# Function to split the binary representation into two equal blocks for DES
def split_into_blocks(binary_data, block_size=64):
    # Ensure the binary data is padded to the correct block size
    if len(binary_data) % block_size != 0:
        padding_size = block_size - (len(binary_data) % block_size)
        binary_data = binary_data.ljust(len(binary_data) + padding_size, '0')
    # Split into two equal halves
    half_size = block_size // 2
    L0 = binary_data[:half_size]
    R0 = binary_data[half_size:]
    return L0, R0

# Split the binary plaintext into two equal blocks
L0, R0 = split_into_blocks(plaintext_binary, block_size=64)

# Print the blocks
print(f"3.iii - L0: {L0}")
print(f"3.iii - R0: {R0}")

#3. IV
# Initial Permutation (IP) table as per the provided image.
IP_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Permute function to rearrange the bits according to the permutation table.
def permute(input_bits, permutation_table):
    return ''.join(input_bits[i - 1] for i in permutation_table)

# Apply the initial permutation on the plaintext binary.
IP_output = permute(plaintext_binary, IP_table)

print(f"3.iv = {IP_output}")

#3.v
# Define the Expansion P-box (E-bit selection table) as provided
expansion_P_box = [
    32, 1,  2,  3,  4,  5,  4,  5,
    6,  7,  8,  9,  8,  9,  10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# Expansion function to expand the R0 block from 32 to 48 bits using the expansion P-box
def expansion_function(block, expansion_table):
    return ''.join(block[i - 1] for i in expansion_table)

# Apply the expansion function to R0
expanded_R0 = expansion_function(R0, expansion_P_box)

# Print the expanded R0 block
print(f"3.v = {expanded_R0}")

#3.vi
PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

key_permutation_table = PC_1

# Apply the key permutation table to the key binary representation
permuted_key = permute(key_binary, key_permutation_table)

# Print the permuted key
print(f"3.vi = {permuted_key}")

# Define the Permuted Choice 2 (PC-2) table
PC_2 = [
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

#3.vii
# Perform circular left shift
def circular_left_shift(key_half, shifts):
    return key_half[shifts:] + key_half[:shifts]

# Initial split of the permuted key into C0 and D0
C0 = permuted_key[:28]
D0 = permuted_key[28:]

# Circular left shifts for round 1 (1 shift as per DES specification)
C1 = circular_left_shift(C0, 1)
D1 = circular_left_shift(D0, 1)

# Combine the halves and apply PC-2 to get K1, the subkey for round 1
K1 = permute(C1 + D1, PC_2)

# Output K1, the final output of the key after round 1 of DES operation
print(f"3.vii = {K1}")


#3.Viii
# XOR function that takes two binary strings and returns their XOR combination
def xor(bin_str1, bin_str2):
    return ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(bin_str1, bin_str2))

# Perform XOR operation between expanded_R0 and K1
xor_output = xor(expanded_R0, K1)

# Print the XOR output
print(f"3.viii = {xor_output}")


#3.ix
# Define S-box tables from S1 to S8
S_boxes = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

#3.x
def sbox_substitution(input_bits):
    output = ''
    for i in range(8):
        # Extract 6 bits for current S-box
        sbox_input = input_bits[i * 6:i * 6 + 6]
        # Convert binary to decimal for row calculation
        row = int(sbox_input[0] + sbox_input[5], 2)
        # Convert binary to decimal for column calculation
        column = int(sbox_input[1:5], 2)
        # Lookup value in S-box table
        sbox_value = S_boxes[i][row][column]
        # Convert S-box value to binary and append to output
        output += format(sbox_value, '04b')
    return output

# Define 48-bit input to S-box substitution (output of part VIII)
sbox_input = xor_output

# Perform S-box substitution
sbox_output = sbox_substitution(sbox_input)

# Print the output of S-box substitution
print(f"3.ix = {sbox_output}")

# Define the straight permutation table
straight_permutation_table = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1,  15, 23, 26, 5,  18, 31, 10,
    2,  8,  24, 14, 32, 27, 3,  9,
    19, 13, 30, 6,  22, 11, 4,  25
]

# Function to perform straight permutation
def straight_permutation(input_bits, permutation_table):
    return ''.join(input_bits[i - 1] for i in permutation_table)

# Output of S-box substitution from part IX (example)
sbox_output = "11001010001100101100100011011100"

# Perform straight permutation
output_after_permutation = straight_permutation(sbox_output, straight_permutation_table)

# Print the output after permutation
print(f"3.x = {output_after_permutation}")

