import math
from math import gcd

# Helper Functions

def is_perfect_power(n: int) -> bool:
    # Step 1: check if n = a^b for integers a > 1, b > 1
    # If yes, n is composite
    if n <= 1:
        return False
    # b <= log_2 n
    max_b = int(math.log2(n))    
    for b in range(2, max_b + 1):
        # approximate integer b-th root of n
        a = int(round(n ** (1.0 / b)))
        # check nearby integers to avoid float errors
        for x in (a - 1, a, a + 1):
            if x > 1 and x ** b == n:
                return True
    return False

def euler_phi(r: int) -> int:
    #Euler's totient for Step 5
    result = r
    x = r
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1
    if x > 1:
        result -= result // x
    return result


def find_smallest_r(n: int) -> int:
    # Step 2: Find the smallest r such that ord_r(n) > (log n)^2
    # We only need to check exponents up to (log n)^2 to see
    # whether n^k ≡ 1 (mod r) happens too early.
    
    if n <= 2:
        return 2

    log2n = math.log2(n)
    max_k = int(log2n ** 2) + 1
    # safe upper bound for small examples
    max_r = int(log2n ** 5) + 3

    for r in range(2, max_r + 1):
        if gcd(n, r) != 1:
            continue
        value = n % r
        good = True
        for _ in range(1, max_k + 1):
            # ord_r(n) ≤ (log n)^2, not good
            if value == 1:
                good = False
                break
            value = (value * n) % r
        if good:
            return r
    # fallback (shouldn't be hit for reasonable n)
    return max_r


# Polynomial arithmetic in (Z/nZ)[X]/(X^r - 1)

def poly_mul(p, q, modn, r):
    #Multiply polynomials p and q modulo (X^r - 1, modn).
    res = [0] * r
    for i, ci in enumerate(p):
        if ci == 0:
            continue
        for j, cj in enumerate(q):
            if cj == 0:
                continue
            idx = (i + j) % r
            res[idx] = (res[idx] + ci * cj) % modn
    return res


def poly_pow(base, exponent, modn, r):
    #Fast exponentiation of a polynomial base^exponent in our ring.
    result = [0] * r
    # polynomial "1"
    result[0] = 1 % modn
    b = base[:]
    e = exponent
    while e > 0:
        if e & 1:
            result = poly_mul(result, b, modn, r)
        b = poly_mul(b, b, modn, r)
        e >>= 1
    return result


def poly_equal(p, q, modn, r) -> bool:
    # Check equality of two polynomials coefficient-wise modulo n.
    for i in range(r):
        if p[i] % modn != q[i] % modn:
            return False
    return True


# Main AKS function

def aks(n: int) -> str:
    #AKS primality test.
    #Returns True if n is PRIME, False if COMPOSITE.

    # small cases
    if n == 2 or n == 3:
        return str(n) + " is a prime"
    if n <= 1:
        return str(n) + " is Composite"

    # Step 1: n is a perfect power?
    if is_perfect_power(n):
        return str(n) + " is Composite"

    # Step 2: find r
    r = find_smallest_r(n)

    # Step 3: 1 < gcd(a, n) < n for some 1 < a ≤ r ?
    for a in range(2, r + 1):
        g = gcd(a, n)
        if 1 < g < n:
            return str(n) + " is Composite"

    # Step 4: if n ≤ r, n is prime
    if n <= r:
        return str(n) + " is a prime"

    # Step 5: for a = 1 to ⌊sqrt(φ(r)) · log n⌋
    phi_r = euler_phi(r)
    # natural log is fine
    limit = int(math.floor(math.sqrt(phi_r) * math.log(n)))
    for a in range(1, limit + 1):
        # (X + a)
        base = [a % n] + [1] + [0] * (r - 2)

        # left side: (X + a)^n mod (X^r - 1, n)
        left = poly_pow(base, n, n, r)

        # right side: X^n + a  mod (X^r - 1, n)
        right = [0] * r
        right[0] = a % n
        right[n % r] = (right[n % r] + 1) % n

        if not poly_equal(left, right, n, r):
            return str(n) + " is Composite"

    # Step 6: PRIME
    return str(n) + " is a prime"


# Example usage

if __name__ == "__main__":
    # Let the user type a number:
    n = int(input("Enter an integer n ≥ 2: "))
    print(aks(n))     # prints True if prime, False if composite