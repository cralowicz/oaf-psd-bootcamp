#test file for isPrime() in is_prime.py
from is_prime import isPrime
import unittest

class TryTesting(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue(isPrime(29))
    def test_is_prime_2(self):
       self.assertTrue(isPrime(25)) 
    def test_is_prime_false(self):
        self.assertFalse(isPrime(22))
    def test_is_prime_4(self):
        self.assertTrue(isPrime('a'))
if __name__ =="__main__": 
    unittest.main()
