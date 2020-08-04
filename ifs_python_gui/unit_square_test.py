import example_generators
import random

num_iters = 10000000


def interval(numer1, denom1, numer2, denom2):
    return [numer1 / denom1, numer2 / denom2]


def is_in_interval(num, interval):
    return interval[0] <= num and num <= interval[1]


def random_diadic_interval():
    denom1 = 2 ** random.randint(1, 12)
    denom2 = 2 ** random.randint(1, 12)

    numer1 = random.randint(0, denom1 - 1)
    numer2 = random.randint(1, denom2)

    while numer1 == numer2 and denom1 == denom2:
        numer1 = random.randint(0, (2 ** exp1) - 1)
        numer2 = random.randint(1, (2 ** exp2) - 1)

    frac1 = numer1 / denom1
    frac2 = numer2 / denom2

    start = min(frac1, frac2)
    end = max(frac1, frac2)

    return [start, end]    


# intervals = [random_diadic_interval() for _ in range(10)]
intervals = [[0, 0.5], [0.5, 1]]

interval_counts = [0 for _ in intervals]

digit_counts = [0, 0]


sequence = example_generators.get_copeland_erdos(2)

w_0 = lambda x: x / 2
w_1 = lambda x: (x + 1) / 2

w = [w_0, w_1]

# point = random.random()
point = .75

print("Starting point: " + str(point))

for i in range(num_iters):
    digit = example_generators.int(next(sequence), base=2)
    point = w[digit](point)

    for j in range(len(intervals)):
        if is_in_interval(point, intervals[j]):
            interval_counts[j] += 1
    digit_counts[digit] += 1

for j in range(len(intervals)):
    interv = intervals[j]
    fraction = interval_counts[j] / num_iters
    dist = interv[1] - interv[0]
    diff = fraction - dist
    print("Interval " + str(interv[0]) + " to " + str(interv[1]) + " distance is " + str(dist) + " got fraction " + str(fraction) + " difference of " + str(diff))

print("Digit counts: " + str(digit_counts))
