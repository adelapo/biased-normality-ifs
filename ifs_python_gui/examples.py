from ifs_classes import *

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

# These will show up in the main app's Examples tab
all_examples = [barnsley_fern, square, sierpinski_triangle]
