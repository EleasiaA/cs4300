"""Task 3: Control structures (if, for, while) """

def classify_number(n):
    #Return 'positive', 'negative', or 'zero
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    
    return "zero"

def first_primes(count = 10):
    #Return the first "count" prime numbers, using a for loop to check each candidate against primes found so far

    primes = []
    candidate = 2
    while len(primes) < count:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break           #no smaller exists
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

def sum_1_to_100():
    #Return the sum of 1 to 100 using a while loop
    total, i = 0, 1
    while i <=100:
        total += i
        i += 1
    return total

def main():
    print(classify_number(5), classify_number(-3), classify_number(0))
    for prime in first_primes(10):
        print(prime)
    print(sum_1_to_100())

if __name__ == "__main__":
    main()