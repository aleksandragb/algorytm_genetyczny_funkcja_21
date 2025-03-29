def binary_to_real(binary_str, min_val, max_val, bits):
    int_val = int(binary_str, 2)
    max_int = 2**bits - 1
    return min_val + (int_val / max_int) * (max_val - min_val)
