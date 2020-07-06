import random


# Copied from numpy source code: https://numpy.org/doc/stable/reference/generated/numpy.base_repr.html
def base_repr(number, base=2, padding=0):
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if base > len(digits):
        raise ValueError("Bases greater than 36 not handled in base_repr.")
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


def get_champernowne(base):
    def champernowne_generator():
        counter = 0
        string_index = 0
        counter_string = base_repr(counter, base=base)
        while True:
            if string_index >= len(counter_string):
                counter += 1
                string_index = 0
                counter_string = base_repr(counter, base=base)

            yield counter_string[string_index]

            string_index += 1

    return champernowne_generator()


def lcm(array):
    largest = max(array)
    m = max(array)
    while any([m % n != 0 for n in array]):
        m += largest
    return m


def get_biased(normal_number, numerators, denominators):
    n = len(numerators)
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


def get_copeland_erdos(base):
    def c_e_generator():
        counter = 2
        string_index = 0
        counter_string = base_repr(counter, base=base)
        while True:
            if string_index >= len(counter_string):
                counter += 1

                while not is_prime(counter):
                    counter += 1

                string_index = 0
                counter_string = base_repr(counter, base=base)

            yield counter_string[string_index]

            string_index += 1

    return c_e_generator()


def get_composites(base):
    def c_e_generator():
        counter = 2
        string_index = 0
        counter_string = base_repr(counter, base=base)
        while True:
            if string_index >= len(counter_string):
                counter += 1

                while is_prime(counter):
                    counter += 1

                string_index = 0
                counter_string = base_repr(counter, base=base)

            yield counter_string[string_index]

            string_index += 1

    return c_e_generator()