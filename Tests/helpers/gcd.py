def euclidean_gcd(a,b):
    r = a % b
    if (r == 0):
        return b
    else:
        print("a: ", a, "   b: ", b, "   c: ",r)
        return euclidean_gcd(b,r)
print(euclidean_gcd(pow(2,2)-1,70))


