#test file for isPrime() in is_prime.py
from is_prime import isPrime
#import unittest

#class TryTesting(unittest.TestCase):
def test_is_prime():
    assert isPrime(29)==True
def test_is_prime_2():
   assert isPrime(25)==True 
def test_is_prime_false():
    assert isPrime(22) ==True
def test_is_prime_4():
    assert isPrime('a')== True
#if __name__ =="__main__": 
  #  unittest.main()
