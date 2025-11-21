from MilerRabin import mrStart
from Fermat import fermatstart
from BailliePSW import baillpswstart
from AKS import askStart

test = input("Choose a test (AKS, BPSW, Fermat, MR): ")
if (test == "AKS"):
    askStart()
elif(test == "BPSW"):
    baillpswstart()
elif(test == "Fermat"):
    fermatstart()
elif(test == "MR"): 
    mrStart
else: print("No test by that name")