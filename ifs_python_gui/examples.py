from ifs_classes import *
import csv
from os import listdir


class Example:
    def __init__(self, name, ifs, prob_numerators, prob_denominators):
        self.name = name
        self.ifs = ifs
        self.prob_numerators = prob_numerators
        self.prob_denominators = prob_denominators


barnsley_fern = Example(
    "Barnsley Fern",
    IteratedFunctionSystem([
        AffineTransformation(0, 0, 0, 0.16, 0, 0),
        AffineTransformation(0.85, 0.04, -0.04, 0.85, 0, 1.6),
        AffineTransformation(0.2, -0.26, 0.23, 0.22, 0, 1.6),
        AffineTransformation(-0.15, 0.28, 0.26, 0.24, 0, 0.44)
    ]),
    [1, 85, 7, 7],
    [100, 100, 100, 100]
)

square = Example(
    "Square",
    IteratedFunctionSystem([
        AffineTransformation(0.5, 0, 0, 0.5, 0, 0),
        AffineTransformation(0.5, 0, 0, 0.5, 0, 50),
        AffineTransformation(0.5, 0, 0, 0.5, 50, 50),
        AffineTransformation(0.5, 0, 0, 0.5, 50, 0)
    ]),
    [1, 1, 1, 1],
    [4, 4, 4, 4]
)

sierpinski_triangle = Example(
    "Sierpinski Triangle",
    IteratedFunctionSystem([
        AffineTransformation(0.5, 0, 0, 0.5, 0, 0),
        AffineTransformation(0.5, 0, 0, 0.5, 0, 50),
        AffineTransformation(0.5, 0, 0, 0.5, 50, 50)
    ]),
    [1, 1, 1],
    [3, 3, 3]
)


def ifs_from_csv(file_name):
    transformations = []
    prob_numerators = []
    prob_denominators = []
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            vals = [float(val) for val in row]
            new_aff_tran = AffineTransformation(*vals[:-2])
            transformations.append(new_aff_tran)
            prob_numerators.append(int(vals[-2]))
            prob_denominators.append(int(vals[-1]))

    return [IteratedFunctionSystem(transformations), prob_numerators, prob_denominators]


def ifs_to_csv(file_name, ifs, prob_numerators, prob_denominators):
    with open(file_name, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for values, num, denom in zip(ifs.transformations, prob_numerators, prob_denominators):
            writer.writerow(values.as_array() + [num] + [denom])


def load_all_examples():
    filenames = [fn for fn in listdir("ifs_examples/") if fn.endswith(".csv")]
    return [Example(fn[:-4], *ifs_from_csv("ifs_examples/" + fn)) for fn in filenames]


# These will show up in the main app's Examples tab
all_examples = load_all_examples()
