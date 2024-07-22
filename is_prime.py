#primeFunction.py

def isPrime(num: int) -> bool:
    if num == 1:
        return False
        print(num, "is not a prime number")
    elif num > 1:
   # check for factors
        for i in range(2,num):
            if (num % i) == 0:
                return False
                print(num,"is not a prime number")
                print(i,"times",num//i,"is",num)
                break
            else:
                return True
                print(num,"is a prime number")
       
# if input number is less than
# or equal to 1, it is not prime
    else:
        return False
        print(num,"is not a prime number")


print(isPrime(29))