import time 
import random 
import string

import matplotlib.pyplot as plt

def add_strints(x: str, y: str) -> str:
    """
    Add two nonnegative integer strings by converting to int.
    This method can be rewritten as a sum/carry adder for a
    single digit addition, pulling characters from the
    input strings. For simplicity now, we just convert the
    whole string to integer, do the addition, and then
    convert the number back to string.
    """
    return str(int(x) + int(y))

def simple_recursive_multiplication(x: str, y: str) -> str:
    """
    Recursive multiplication for nonnegative integer strings.
    Assumptions:
      - len(x) == len(y)
      - len(x) is a power of two
      - x and y contain only digits
    Uses:
      xy = ac*10^n + (ad+bc)*10^(n/2) + bd
    """
    # Number of digits in x, y
    n = len(x)
    # Base case
    if n == 1:
        return str(int(x) * int(y))
    # Middle of x, y for splitting them in left/right halves
    m = n // 2
    # Divide x, y into left/right halves
    a = x[:m]
    b = x[m:]
    c = y[:m]
    d = y[m:]
    # Compute the partial solution
    ac = simple_recursive_multiplication(a, c)
    ad = simple_recursive_multiplication(a, d)
    bc = simple_recursive_multiplication(b, c)
    bd = simple_recursive_multiplication(b, d)
    # Conquer the partial solutions
    ad_plus_bc = add_strints(ad, bc)
    # Multiply by powers of 10 via appending zeros (string shift).
    term1 = ac + ("0" * n)
    term2 = ad_plus_bc + ("0" * m)
    # Final sum (Using int conversion for addition to keep things simple)
    return str(int(term1) + int(term2) + int(bd))

def k_multiply(x: str, y: str) -> str:
    """
    Karatsuba recursive multiplication for nonnegative integer strings.

    Uses the optimized formula with only 3 recursive calls:
    xy = ac*10^n + ((a+b)(c+d) - ac - bd)*10^(n/2) + bd

    Includes padding logic using .zfill to handle cases where recursive
    sums (a + b) and (c + d) result in strings of unequal length.
    """
    n = len(x)

    if n == 1:
        return str(int(x) * int(y))
    
    m = n // 2 
    
    a = x[:m]
    b = x[m:]
    c = y[:m]
    d = y[m:]
   
    half_len = len(b)

    a_plus_b = str(int(a) + int(b))
    c_plus_d = str(int(c) + int(d))
   
    max_len = max(len(a_plus_b), len(c_plus_d))

    a_plus_b = a_plus_b.zfill(max_len)
    c_plus_d = c_plus_d.zfill(max_len)

    a_c = k_multiply(a, c)
    b_d = k_multiply(b, d)
    
    a_b_times_c_d = k_multiply(a_plus_b, c_plus_d)
    
    term1 = a_c + ("0" * (2 * half_len))
    term2 = str(int(a_b_times_c_d) - int(a_c) - int(b_d)) + ("0" * half_len)

    return str(int(term1) + int(term2) + int(b_d))

def get_random_string(n):
    """Returns a random string of digits of length n."""
    return ''.join(random.choices(string.digits, k=n))

def benchmark():
    """
    Benchmark method to compare simple_recursive_multiplication with k_multiply.

    Generates two random strings of n length and times the respective
    execution times.

    Generates graph for visual comparison and prints table of values.
    """
    n_list = []
    k_list = []
    simple_list = []
    print(f"{'n':<10} | {'Simple (s)':<15} | {'Karatsuba (s)':<15}")
    print("-" * 45)

    n = 4
    while n <= 2048:
        x = get_random_string(n)
        y = get_random_string(n)

        start = time.time()
        simple_recursive_multiplication(x, y)
        end = time.time()
        simple_time = end - start

        start = time.time()
        k_multiply(x, y)
        end = time.time()
        karatsuba_time = end - start
        
        n_list.append(n)
        k_list.append(karatsuba_time)
        simple_list.append(simple_time)

        print(f"{n:<10} | {simple_time:<15.6f} | {karatsuba_time:<15.6f}")

        n *= 2
    plot_results(n_list, simple_list, k_list)

def plot_results(n_values, simple_times, karatsuba_times):
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, simple_times, marker='o', label='Simple Recursive (O(n^2))')
    plt.plot(n_values, karatsuba_times, marker='s', label='Karatsuba (O(n^1.58))')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xticks(n_values, labels=n_values)
    plt.show()


if __name__ == "__main__":
    tests = [
            ("12", "34"),
            ("99", "99"),
            ("0123", "0456"),
            ("1234", "5678"),
            ("0000", "0000"),
            ("1111", "0001"),
            ("1234567890123456", "9876543210123456"),
            ("12345678901234561234567890123456", "12345678901234561234567890123456"),
            ("1234567890123456123456789012345612345678901234561234567890123456", "1234567890123456123456789012345612345678901234561234567890123456"),
        ]

    for x, y in tests:
        # Compare against Python int multiplication for correctness.
        got = k_multiply(x, y)
        want = str(int(x) * int(y))
        print(f"{x} * {y} = {got}  (ok={got == want})")

    benchmark()
