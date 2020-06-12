import tkinter as tk

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class AffineTransformation:
    """
     _      _  _ _       _   _
    | a    b || x |     |  e  |
    |        ||   |  +  |     |
    | c    d || y |     |  f  |
     -      -  - -       -   -
     
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

class IteratedFunctionSystem:
    def __init__(self, transformations):
        self.transformations = transformations

        self.size = len(transformations)

    def get_image(self, image_width, image_height, num_iters, generator,
                  starting_point=Coordinate(0, 0), fg_color="#00ff00", bg_color="#000000"):

        img = tk.PhotoImage(width=image_width, height=image_height)

        # Set background color
        img.put(bg_color, to=(0, 0, image_width, image_height))

        # Calculation of points
        all_points = [starting_point]

        current_point = starting_point

        for i in range(num_iters):
            index = int(next(generator), base=self.size)

            t = self.transformations[index]
            current_point = t.transform(current_point)

            all_points.append(current_point)

        # Stretch to fit image
        min_x = min(all_points, key=lambda pt: pt.x).x
        max_x = max(all_points, key=lambda pt: pt.x).x

        min_y = min(all_points, key=lambda pt: pt.y).y
        max_y = max(all_points, key=lambda pt: pt.y).y

        # stretch = AffineTransformation(max_x - min_x, 0, 0, max_y - min_y, min_x, min_y)
        fractal_width = max_x - min_x
        fractal_height = max_y - min_y

        fractal_size = max(fractal_width, fractal_height)

        drawn_points = []
        for pt in all_points:
            new_x = ((pt.x - min_x) / fractal_size) * image_width
            new_y = ((pt.y - min_y) / fractal_size) * image_height

            drawn_points.append(Coordinate(new_x, new_y))

        for pt in drawn_points:
            img.put(fg_color, (round(pt.x), round(pt.y)))

        return img
