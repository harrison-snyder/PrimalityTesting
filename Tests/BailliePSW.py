"""
Implementation of the Baillie-PSW primality test

This implementation has been adapted from: https://github.com/armchaircaver/Baillie-PSW/tree/main
Several functions have been adapted from various sources on the internet. They have been cited accordingly. 

"""
from MillerRabin import mrTest
from Crypto.Util.number import getPrime

# from https://stackoverflow.com/questions/44531084/python-check-if-a-number-is-a-square
def is_square(n):
    if n < 0:
        return False
    if n == 0:
        return True
    x, y = 1, n
    while x + 1 < y:
        mid = (x+y)//2
        if mid**2 < n:
            x = mid
        else:
            y = mid
    return n == x**2 or n == (x+1)**2
#-------------------------------------------------------------------------------

# adapted from https://rosettacode.org/wiki/Jacobi_symbol#Python
def jacobi(d, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    d %= n
    result = 1
    while d != 0:
        while d % 2 == 0:
            d /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        d, n = n, d
        if d % 4 == 3 and n % 4 == 3:
            result = -result
        d %= n
    if n == 1:
        return result
    else:
        return 0
#-------------------------------------------------------------------------------

def D_chooser(n):
  #Choose a D value suitable for the Baillie-PSW test
  D = 5
  j = jacobi(D, n)

  while j > 0:
    D += 2 if D > 0 else -2
    D *= -1

    if D==-15 :
      # check for a square
      if is_square(n):
        # The value of D isn't 0, but we are just communicating
        # that we have found a square
        return (0,0) 

    j = jacobi(D, n)
  return (D,j)
#-------------------------------------------------------------------------------

div2mod = lambda x,n: ((x+n)>>1)%n if x&1 else (x>>1)%n
#-------------------------------------------------------------------------------
# U, V, Lucas Sequences 
def U_V_subscript(k, n, P, D):
  U=1
  V=P
  digits = bin(k)[2:]

  for digit in digits[1:]:
    U, V = (U*V) % n,  div2mod(V*V + D*U*U, n)

    if digit == '1':
      U,V = div2mod(P*U + V, n), div2mod(D*U + P*V, n)
  return U, V
#-------------------------------------------------------------------------------
# Lucas Test for probable and pseudo primes
def lucas_pp(n, D, P, Q):                                                                                                                                                                                                                         
  assert n & 1
  U, V = U_V_subscript(n+1, n, P, D)
  return U==0

#-------------------------------------------------------------------------------
def baillie_psw(n):

  if n <= 1: return False
  if n&1==0:
    return n==2

  # need to test small primes as the D chooser might not find
  # a suitable value for small primes
  for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]:
    if n % p == 0:
      return n==p

  # Proabble prime test for base = 2 (Miller Rabin that we have used)  
  if not mrTest(n, 2):
    return False

  
  D,j = D_chooser(n)
  if j==0:
    return False 

  
  return lucas_pp(n, D, 1, (1-D)//4) 
#-------------------------------------------------------------------------------

def baillpswstart():
    test = int(input("Give a number to be tested with Baillie-PSW: "))
    baillie_psw(test)

prime = getPrime(1024)
assert baillie_psw(prime) == True
assert baillie_psw(19) == True
