#from Crypto.Util.number import getPrime
#Fermat's Primality Testing
import random
from helpers.gcd import euclidean_gcd
import time


#basic implementation
def FPT(prime,number_of_tests):
    random_number = random.sample(range(2,prime-2), number_of_tests) 
                        #^ Choose random numbers to test
    for i in range(number_of_tests):
        if (pow(random_number[i],prime-1,prime) != 1):
            return True #Returns Composite
    return False        #Probably Prime



# this is the long one 

#Fermat's Primality Testing
import random


def fermat(prime,number_of_tests):
#catches if trying to do more than prime - 3 tests
    if (number_of_tests > (prime - 3)):
        print("Use at max tests less than your prime ", "(", prime - 3,")")
        return
    #Checking, for a random number "a" between 2 and prime candidate minus 2, if a^(prime candidate-1)=1mod(prime candidate)
    random_number = random.sample(range(2,prime-2), number_of_tests)

    for i in range(number_of_tests):
        
        print("testing ", random_number[i], " as a witness" )
        print( "gcd:", euclidean_gcd(prime,random_number[i]))
        if (pow(random_number[i],prime-1,prime) != 1):
            print(prime, "is composite")
            return
        print(random_number[i], "is not a witness")
    print("probably prime")
    return





def fermatstart():
    prime = int(input("Give a number greater than 3 to test: "))
    #needs to be 3 less than the prime number because we can only test [2, prime -2]
    number_of_tests = int(input("Enter your # tests: "))
    print(type(number_of_tests))

    fermat(prime,number_of_tests)


def fermatStartTimed():
    prime = int(input("Give a number greater than 3 to test: "))
    #needs to be 3 less than the prime number because we can only test [2, prime -2]
    number_of_tests = int(input("Enter your # tests: "))
    start_time = time.time()
    fermat(prime,number_of_tests)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    return elapsed_time


#prime = getPrime(29)
#assert fermat(prime, 10) == True
#assert fermat(11, 5) == True
#fermatstart()