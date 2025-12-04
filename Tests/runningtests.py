from MilerRabin import mrStart,mrStartTimed
from Fermat import fermatstart,fermatStartTimed
from BailliePSW import baillpswstart,baillpswstartTimed
from AKS import aksStart, aksStartTimed
import time

test = input("Choose a test (AKS, BPSW, Fermat, MR): ")
t = input(" \"Timed\" or not?: ")
if (t == "Timed"):
    time = 0
    if (test == "AKS"):
        time = aksStartTimed()
    elif(test == "BPSW"):
        time = baillpswstartTimed()
    elif(test == "Fermat"):
        time = fermatStartTimed()
    elif(test == "MR"): 
        time = mrStartTimed()
    else: print("No test by that name")
    print("time taken :  ",time )
else: 
    if (test == "AKS"):
        aksStart()
    elif(test == "BPSW"):
        baillpswstart()
    elif(test == "Fermat"):
        fermatstart()
    elif(test == "MR"): 
        mrStart
    else: print("No test by that name")