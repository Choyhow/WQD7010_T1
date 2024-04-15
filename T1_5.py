# Given values
S = [7, 2, 5, 1, 0, 3, 6, 4]
K = [2, 0, 1]
PT = [5, 3, 1, 6]

# Initial Permutation of the S-Array
j = 0
for i in range(len(S)):
    j = (j + S[i] + K[i % len(K)]) % len(S)
    S[i], S[j] = S[j], S[i]  # Swap values at indices i and j

# The S-Array after the initial permutation
initial_permuted_S = S.copy()

# Keystream Generation (Simplified RC4 Algorithm)
i = j = 0
keystream = []
for byte in PT:
    i = (i + 1) % len(S)
    j = (j + S[i]) % len(S)
    S[i], S[j] = S[j], S[i]  # Swap values at indices i and j
    t = (S[i] + S[j]) % len(S)
    keystream.append(S[t])

# Ciphertext Calculation (XOR Plaintext with Keystream)
ciphertext = [pt_byte ^ ks_byte for pt_byte, ks_byte in zip(PT, keystream)]


print(f"5.i  = {initial_permuted_S}")
print(f"5.ii  = {keystream}")
print(f"5.iii  = {ciphertext}")