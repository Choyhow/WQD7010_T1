# Define the given key in hexadecimal
hex_key = "E0E0E0E0F1F1F1F1"

# Convert the key to binary
binary_key = bin(int(hex_key, 16))[2:].zfill(64) # Ensure it is 64 bits long

# The parity bit drop table from Figure 1 (minus the 8 bits that are dropped)
parity_bit_drop_table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# The key-permutation compression table from Figure 2
key_permutation_compression_table = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

# Function to apply the parity bit drop process
def apply_parity_bit_drop(binary_key, parity_bit_drop_table):
    return ''.join([binary_key[i-1] for i in parity_bit_drop_table])

# Function to apply the key-permutation compression
def apply_key_permutation_compression(key_after_drop, key_permutation_compression_table):
    return ''.join([key_after_drop[i-1] for i in key_permutation_compression_table])

# Apply parity bit drop
key_after_drop = apply_parity_bit_drop(binary_key, parity_bit_drop_table)

# Apply key-permutation compression
compressed_key = apply_key_permutation_compression(key_after_drop, key_permutation_compression_table)


print(f"2.i = {key_after_drop}")
print(f"2.ii = {compressed_key}")
