# PrimalityTesting
A comprehensive investigation of different primality tests

## Introduction

Prime numbers are fundamental within cryptography, with a variety of the modern day encryption algorithms keeping our information secure relying on primality testing for their utility. Primality testing in public key encryption is the process of determining whether a number is prime, meaning it is only divisible by one or itself. Both used as a tool to validate prime parameters, or as part of the algorithm used to generate random prime numbers, primality tests are found nearly universally in cryptography. Efficient primality tests are needed for generating keys used in many modern cryptographic systems. The difficulty of the discrete logarithm problem (DLP) in many cryptographic applications is directly tied to the use of extremely large prime numbers and how they are generated. The hardness of this problem, which is crucial for public-key cryptography, is significantly reduced if the group is not carefully constructed.

In this report, we will go through a few of the most widely known primality testing algorithms, offering an overview followed by an implementation. We will compare their time complexities and accuracies and look into areas where these tests might fail and what implications that might have in the context of public key cryptography. 

## Code Usage 

###   Fermat's Primality Test

###   AKS Primality Test

The AKS.py file is standalone and only needs to be run as a single python file. It asks for the number in question within the terminal, and outputs whether or not it is prime or composite. The comments within the code can help link to the process of AKS primality testing to explain the linkage and how it operates.

###   Miller Rabin Primality Test

###   Ballie PSW

###   Helper Functions
####     Extended Euclidean Algorithim



