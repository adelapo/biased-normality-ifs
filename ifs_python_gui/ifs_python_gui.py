import random
import tkinter as tk
from numpy import base_repr
from math import sqrt

from ifs_classes import *

import examples

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600

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
    for i in range(2, int(sqrt(n)) + 1):
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
            
root = tk.Tk()

# Transformations frame

class TransformationsFrame(tk.LabelFrame):
    def __init__(self, parent, **kwargs):
        tk.LabelFrame.__init__(self, parent, **kwargs)

        self.parent = parent

        self.num_selector_frame = tk.Frame(self)
        self.num_selector_frame.pack()

        self.num_selector_label = tk.Label(self.num_selector_frame, text="Number of transformations:")
        self.num_selector_label.grid(row=1, column=1)

        self.num_selector_entry = tk.Entry(self.num_selector_frame, width=4)
        self.num_selector_entry.grid(row=1, column=2)

        self.num_selector_entry.insert(0, "3")

        self.transformation_entries = []

        self.num_selector_button = tk.Button(self.num_selector_frame, text="Select", command=self.num_selected)
        self.num_selector_button.grid(row=1, column=3)

        self.affine_vals_frame = tk.Frame(self)
        self.affine_vals_frame.pack()

        self.num_selected()

    def num_selected(self):
        num = int(self.num_selector_entry.get())

        affine_val_labels = ["a", "b", "c", "d", "e", "f"]

        for w in self.affine_vals_frame.winfo_children():
            w.destroy()

        for col in range(len(affine_val_labels)):
            col_label = tk.Entry(self.affine_vals_frame, width=8, justify=tk.CENTER)
            col_label.grid(row=0, column=col)
            col_label.insert(0, affine_val_labels[col])
            col_label.config(state=tk.DISABLED, disabledforeground="black")

        p_col_label = tk.Entry(self.affine_vals_frame, width=19, justify=tk.CENTER)
        p_col_label.grid(row=0, column=len(affine_val_labels), columnspan=3, padx=(10, 0))
        p_col_label.insert(0, "p=r/s")
        p_col_label.config(state=tk.DISABLED, disabledforeground="black")

        self.transformation_entries = []

        for row in range(num):
            row_entries = []

            for col in range(len(affine_val_labels)):
                col_entry = tk.Entry(self.affine_vals_frame, width=8, justify=tk.CENTER)
                col_entry.grid(row=row+1, column=col)

                row_entries.append(col_entry)

            p_numerator_entry = tk.Entry(self.affine_vals_frame, width=8, justify=tk.RIGHT)
            p_numerator_entry.grid(row=row+1, column=len(affine_val_labels), padx=(10, 0))

            row_entries.append(p_numerator_entry)

            p_slash_label = tk.Label(self.affine_vals_frame, text="/")
            p_slash_label.grid(row=row+1, column=len(affine_val_labels)+1)

            p_denominator_entry = tk.Entry(self.affine_vals_frame, width=8, justify=tk.LEFT)
            p_denominator_entry.grid(row=row+1, column=len(affine_val_labels)+2)

            row_entries.append(p_denominator_entry)

            self.transformation_entries.append(row_entries)

    def get_ifs(self):
        transformations = []
        prob_numerators = []
        prob_denominators = []

        for row in self.transformation_entries:
            try:
                a, b, c, d, e, f, p_num, p_den = list(map(lambda entry: float(entry.get()), row))
            except ValueError:
                return

            transformations.append(AffineTransformation(a, b, c, d, e, f))
            prob_numerators.append(int(p_num))
            prob_denominators.append(int(p_den))            

        return IteratedFunctionSystem(transformations), prob_numerators, prob_denominators
        
transformations_frame = TransformationsFrame(root, text="Affine Transformations")
transformations_frame.pack(pady=10)

# Generator Frame
generator_frame = tk.LabelFrame(root, text="Generator Options")
generator_frame.pack()

num_iters_label = tk.Label(generator_frame, text="Number of iterations:")
num_iters_label.grid(row=1, column=1)

num_iters_entry = tk.Entry(generator_frame, width=10)
num_iters_entry.grid(row=1, column=2)

num_iters_entry.insert(0, 100000)

generator_label = tk.Label(generator_frame, text="Select a generator:")
generator_label.grid(row=2, column=1)

generator_options = ["Pseudo-random number generator",
                     "Champernowne's constant",
                     "Copeland-Erdos constant",
                     "Biased normal (Champernowne)",
                     "Biased normal (Copeland-Erdos)"]

generator_var = tk.StringVar()
generator_var.set(generator_options[0])

generator_menu = tk.OptionMenu(generator_frame, generator_var, *generator_options)
generator_menu.grid(row=2, column=2)

go_button = tk.Button(root, text="Go", width=10)
go_button.pack(pady=10)

black_img = tk.PhotoImage(width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
black_img.put("#000000", to=(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))

fractal_label = tk.Label(root, image=black_img)
fractal_label.image = black_img
fractal_label.pack()

def go_button_pressed():
    user_input = transformations_frame.get_ifs()

    if user_input is None:
        return
    
    ifs, prob_numerators, prob_denominators = transformations_frame.get_ifs()

    gen_op = generator_var.get()

    if gen_op == "Champernowne's constant":
        gen = get_champernowne(ifs.size)
    elif gen_op == "Copeland-Erdos constant":
        gen = get_copeland_erdos(ifs.size)
    elif gen_op == "Biased normal (Champernowne)":
        champ = get_champernowne(lcm(prob_denominators))
        gen = get_biased(champ, prob_numerators, prob_denominators)
    elif gen_op == "Biased normal (Copeland-Erdos)":
        c_e = get_copeland_erdos(lcm(prob_denominators))
        gen = get_biased(c_e, prob_numerators, prob_denominators)
    else:
        gen = get_random_generator(ifs.size, [r / s for r, s in zip(prob_numerators, prob_denominators)])

    img = ifs.get_image(IMAGE_WIDTH, IMAGE_HEIGHT, int(num_iters_entry.get()), gen)

    fractal_label.config(image=img)
    fractal_label.image = img    

go_button.config(command=go_button_pressed)

# Menu
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="About")
file_menu.add_command(label="Help")
file_menu.add_separator()
file_menu.add_command(label="Save Image")
menu_bar.add_cascade(label="File", menu=file_menu)

examples_menu = tk.Menu(menu_bar, tearoff=0)

for example in examples.all_examples:
    def load_example(example=example):
        transformations_frame.num_selector_entry.delete(0, tk.END)
        transformations_frame.num_selector_entry.insert(0, example.ifs.size)
        transformations_frame.num_selected()

        #for row in transformations_frame.transformation_entries:
        for i in range(example.ifs.size):
            row = transformations_frame.transformation_entries[i]

            row[0].insert(0, example.ifs.transformations[i].a)
            row[1].insert(0, example.ifs.transformations[i].b)
            row[2].insert(0, example.ifs.transformations[i].c)
            row[3].insert(0, example.ifs.transformations[i].d)
            row[4].insert(0, example.ifs.transformations[i].e)
            row[5].insert(0, example.ifs.transformations[i].f)

            row[6].insert(0, example.prob_numerators[i])
            row[7].insert(0, example.prob_denominators[i])

    examples_menu.add_command(label=example.name, command=load_example)

menu_bar.add_cascade(label="Examples", menu=examples_menu)

root.config(menu=menu_bar)

root.wm_title("IFS Code Visualizer")

root.mainloop()
