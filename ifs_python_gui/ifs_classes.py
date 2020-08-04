from tkinter import PhotoImage
from example_generators import base_repr, int


# From https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB_alternative
def hsv_to_rgb(h, s, v):
    # h: hue: 0 to 360
    # s: saturation: 0 to 1
    # v: value: 0 to 1
    def f(n):
        k = (n + (h / 60)) % 6
        return v - (v * s * max(0, min(k, 4 - k, 1)))
    r, g, b = int(f(5) * 255), int(f(3) * 255), int(f(1) * 255)
    r, g, b = base_repr(r, base=16).zfill(2), base_repr(g, base=16).zfill(2), base_repr(b, base=16).zfill(2)
    return "#" + r + g + b


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class AffineTransformation:
    """
     _      _  _ _       _   _      _           _
    | a    b || x |     |  e  |    | ax + by + e |
    |        ||   |  +  |     |  = |             |
    | c    d || y |     |  f  |    | cx + dy + f |
     -      -  - -       -   -      -           -
     
    """
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def transform(self, coord):
        new_x = self.a * coord.x + self.b * coord.y + self.e
        new_y = self.c * coord.x + self.d * coord.y + self.f

        return Coordinate(new_x, new_y)

    def as_array(self):
        return [self.a, self.b, self.c, self.d, self.e, self.f]


class IteratedFunctionSystem:
    def __init__(self, transformations):
        self.transformations = transformations

        self.size = len(transformations)

    def get_image(self, image_width, image_height, num_iters, generator, starting_point=Coordinate(0, 0),
                  bg_color="#000000", fg_color="#00FF00", colors=True, first_transformations=100):
        img = PhotoImage(width=image_width, height=image_height)

        # Set background color
        img.put(bg_color, to=(0, 0, image_width, image_height))

        # Calculation of points
        all_points = [starting_point]
        all_transformations = [0]
        gen_str = ""

        current_point = starting_point

        for i in range(num_iters):
            gen_val = next(generator)
            index = int(gen_val, base=self.size)

            t = self.transformations[index]
            current_point = t.transform(current_point)

            all_points.append(current_point)
            all_transformations.append(index)
            gen_str += gen_val

        # Stretch to fit image
        min_x = min(all_points, key=lambda pt: pt.x).x
        max_x = max(all_points, key=lambda pt: pt.x).x

        min_y = min(all_points, key=lambda pt: pt.y).y
        max_y = max(all_points, key=lambda pt: pt.y).y

        fractal_width = max_x - min_x
        fractal_height = max_y - min_y

        fractal_size = max(fractal_width, fractal_height)

        drawn_points = []
        draw_colors = []

        for pt, index in zip(all_points, all_transformations):
            new_x = ((pt.x - min_x) / fractal_size) * image_width
            new_y = ((pt.y - min_y) / fractal_size) * image_height

            new_y = image_height - new_y

            drawn_points.append(Coordinate(new_x, new_y))
            draw_colors.append(hsv_to_rgb(index * 360 / self.size, 1, 1))

        # Draw points
        if colors:
            for pt, dot_color in zip(drawn_points, draw_colors):
                img.put(dot_color, (round(pt.x), round(pt.y)))
        else:
            for pt in drawn_points:
                img.put(fg_color, (round(pt.x), round(pt.y)))

        return img, gen_str[:first_transformations]
