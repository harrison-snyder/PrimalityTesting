
from helpers.gcd import euclidean_gcd

# Uses gcd from helper functions folder


#The Miller-Rabin Test
#   Input:
#       pc  - an integer to be tested for primality 
#       a - an integer for pc potential witness of a being 
#   Returns:
#       Composite if the number is composite
#       Failure if the witness does not prove compositeness 
def mrTest(pc,a):
    ast = a
    if (pc % 2 == 0): # check if candidate is even
        print(pc, " is composite from being even")
        return
    d = euclidean_gcd(pc,a) 
    if(d > 1 and d < pc): #Check if the gcd is 1, composite if not
        print(pc, " is composite from gcd")
        return
    n1 = pc - 1
    q = n1
    k = 0
    while (q % 2): #Finding q and k for n - 1 = 2^k * q
        q=q/2
        k+=1
    ast = pow(a,q,pc)
    if (ast == 1):
        print("Test failed, ", ast, " is not a witness for ", pc, " being composite")
        return
    for i in range(k):
        if (ast == pc - 1):
            print("Test failed, ", ast, " is not a witness for ", pc, " being composite")
            return
        ast = pow(ast,2,pc)
    
    print(a, "is a witness for ", pc, "being composite")



def mrStart():
    pc = int(input("Give a prime candidate to test: "))
    a = int(input("Enter your witness: "))
    mrTest(pc,a)

