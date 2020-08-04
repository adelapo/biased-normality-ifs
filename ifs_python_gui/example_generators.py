import random

digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzαβγδεζηθι!@#$%^&*()`~,./<>?;\':\"[]{}+\\|'


# Copied from numpy source code: https://numpy.org/doc/stable/reference/generated/numpy.base_repr.html
def base_repr(number, base=2, padding=0):
    if base > len(digits):
        raise ValueError("Bases greater than 100 not handled in base_repr.")
    elif base < 2:
        raise ValueError("Bases less than 2 not handled in base_repr.")

    num = abs(number)
    res = []
    while num:
        res.append(digits[num % base])
        num //= base
    if padding:
        res.append('0' * padding)
    if number < 0:
        res.append('-')
    return ''.join(reversed(res or '0'))


python_int = int


def int(x, base=10):
    if type(x) != str:
        return python_int(x)

    if base <= 36 or base > len(digits) or len(x) == 0:
        return python_int(x, base=base)

    if x[0] == "-":
        return -int(x[1:], base=base)

    num = 0
    for i in range(len(x)):
        num += digits.index(x[i]) * (base ** (len(x) - i - 1))

    return num


def concat_generator(generator):
    while True:
        current_value = next(generator)

        for digit in str(current_value):
            yield digit


def get_champernowne(base):
    def counter_generator():
        counter = 0
        while True:
            yield base_repr(counter, base=base)
            counter += 1
    return concat_generator(counter_generator())


def get_besicovitch(base):
    def square_generator():
        counter = 1
        while True:
            yield base_repr(counter * counter, base=base)
            counter += 1
    return concat_generator(square_generator())


def get_copeland_erdos(base):
    def prime_generator_slow():
        yield "2"

        counter = 3

        while True:
            if is_prime(counter):
                yield base_repr(counter, base=base)
            counter += 2

    # Adapted from http://code.activestate.com/recipes/117119-sieve-of-eratosthenes/#c4
    def prime_generator():
        yield base_repr(2, base=base)
        D = {}
        q = 3

        while True:
            p = D.pop(q, 0)
            if p:
                x = q + p
                while x in D:
                    x += p
                D[x] = p
            else:
                yield base_repr(q, base=base)
                D[q * q] = 2 * q
            q += 2

    return concat_generator(prime_generator())


def get_random_generator(base, probs):
    def random_generator():
        while True:
            prob = 0
            rand = random.random()

            result_found = False

            for i in range(len(probs)):
                prob += probs[i]
                if rand < prob and not result_found:
                    result = i
                    result_found = True

            yield str(result)

    return random_generator()


def lcm(array):
    largest = max(array)
    m = max(array)
    while any([m % n != 0 for n in array]):
        m += largest
    return m


def get_biased(normal_number, numerators, denominators):
    n = len(denominators)
    d = lcm(denominators)
    g = ""
    for i in range(n):
        count = numerators[i] * (d / denominators[i])
        g += base_repr(i, base=n) * int(count)

    def biased_generator():
        while True:
            next_index = next(normal_number)
            yield g[int(next_index, base=d)]

    return biased_generator()


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


all_generators = [("Champernowne's constant", get_champernowne),
                  ("Copeland-Erdos constant", get_copeland_erdos),
                  ("Besicovitch's sequence", get_besicovitch)]
