import tkinter.filedialog
import tkinter as tk
from example_generators import *
from ifs_classes import *

import examples

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600

root = tk.Tk()


# Adapted from https://blog.tecladocode.com/tkinter-scrollable-frames/
class ScrollableLabelFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=150)
        self.canvas = canvas

        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all"),
                width=canvas.bbox("all")[2] - canvas.bbox("all")[0]
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


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

        self.affine_vals_scroll_frame = ScrollableLabelFrame(self)
        self.affine_vals_scroll_frame.pack()

        self.affine_vals_frame = self.affine_vals_scroll_frame.scrollable_frame

        self.num_selected()

    def num_selected(self):
        num = int(self.num_selector_entry.get())

        affine_val_labels = ["a", "b", "c", "d", "e", "f"]

        for w in self.affine_vals_frame.winfo_children():
            w.destroy()

        num_label = tk.Entry(self.affine_vals_frame, width=8, justify=tk.CENTER)
        num_label.grid(row=0, column=0)
        num_label.config(state=tk.DISABLED, disabledforeground="black")

        for col in range(len(affine_val_labels)):
            col_label = tk.Entry(self.affine_vals_frame, width=8, justify=tk.CENTER)
            col_label.grid(row=0, column=col+1)
            col_label.insert(0, affine_val_labels[col])
            col_label.config(state=tk.DISABLED, disabledforeground="black")

        p_col_label = tk.Entry(self.affine_vals_frame, width=19, justify=tk.CENTER)
        p_col_label.grid(row=0, column=len(affine_val_labels)+1, columnspan=3, padx=(10, 0))
        p_col_label.insert(0, "p=r/s")
        p_col_label.config(state=tk.DISABLED, disabledforeground="black")

        self.transformation_entries = []

        for row in range(num):
            row_entries = []

            row_label = tk.Entry(self.affine_vals_frame, width=8, justify=tk.CENTER)
            row_label.grid(row=row+1, column=0)
            row_label.insert(0, base_repr(row, base=36))
            row_label.config(state=tk.DISABLED, disabledforeground="black")

            for col in range(len(affine_val_labels)):
                col_entry = tk.Entry(self.affine_vals_frame, width=8, justify=tk.CENTER)
                col_entry.grid(row=row+1, column=col+1)

                row_entries.append(col_entry)

            p_numerator_entry = tk.Entry(self.affine_vals_frame, width=8, justify=tk.RIGHT)
            p_numerator_entry.grid(row=row+1, column=len(affine_val_labels)+1, padx=(10, 0))

            row_entries.append(p_numerator_entry)

            p_slash_label = tk.Label(self.affine_vals_frame, text="/")
            p_slash_label.grid(row=row+1, column=len(affine_val_labels)+2)

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
transformations_frame.grid(row=1, column=1, rowspan=2, pady=(0, 10))

generator_options = ["Pseudo-random number generator",
                     "Champernowne's constant",
                     "Copeland-Erdos constant",
                     "Composites",
                     "Biased normal (Champernowne)",
                     "Biased normal (Copeland-Erdos)",
                     "Biased normal (Composites)"]

generator_var = tk.StringVar()
generator_var.set(generator_options[0])

generator_menu = tk.OptionMenu(root, generator_var, *generator_options)
generator_menu.config(width=50)
generator_menu.grid(row=1, column=2)

# Drawing Options Frame
drawing_frame = tk.LabelFrame(root, text="Drawing Options")
drawing_frame.grid(row=2, column=2)

num_iters_label = tk.Label(drawing_frame, text="Number of iterations:")
num_iters_label.grid(row=1, column=1)

num_iters_entry = tk.Entry(drawing_frame, width=10)
num_iters_entry.grid(row=1, column=2)

num_iters_entry.insert(0, 100000)

show_colors_var = tk.IntVar()
show_colors_var.set(1)

show_colors_cbox = tk.Checkbutton(drawing_frame, text="Color for each transformation", variable=show_colors_var)
show_colors_cbox.grid(row=2, column=1, columnspan=2)

go_button = tk.Button(root, text="Go", width=10)
go_button.grid(row=3, column=1, columnspan=2, pady=10)

black_img = tk.PhotoImage(width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
black_img.put("#000000", to=(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))

first_transformations_label = tk.Entry(root, width=100, state=tk.DISABLED, disabledforeground="black")
first_transformations_label.grid(row=4, column=1, columnspan=2, pady=(0, 10))

fractal_label = tk.Label(root, image=black_img)
fractal_label.image = black_img
fractal_label.grid(row=5, column=1, columnspan=2)


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
    elif gen_op == "Composites":
        gen = get_composites(ifs.size)
    elif gen_op == "Biased normal (Champernowne)":
        champ = get_champernowne(lcm(prob_denominators))
        gen = get_biased(champ, prob_numerators, prob_denominators)
    elif gen_op == "Biased normal (Copeland-Erdos)":
        c_e = get_copeland_erdos(lcm(prob_denominators))
        gen = get_biased(c_e, prob_numerators, prob_denominators)
    elif gen_op == "Biased normal (Composites)":
        c_e = get_composites(lcm(prob_denominators))
        gen = get_biased(c_e, prob_numerators, prob_denominators)
    else:
        gen = get_random_generator(ifs.size, [r / s for r, s in zip(prob_numerators, prob_denominators)])

    img, gen_str = ifs.get_image(IMAGE_WIDTH, IMAGE_HEIGHT, int(num_iters_entry.get()),
                                 gen, colors=show_colors_var.get() == 1, first_transformations=100)

    first_transformations_label.config(state=tk.NORMAL)
    first_transformations_label.delete(0, tk.END)
    first_transformations_label.insert(0, gen_str)
    first_transformations_label.config(state=tk.DISABLED)

    fractal_label.config(image=img)
    fractal_label.image = img    


go_button.config(command=go_button_pressed)


# Menu Commands
def save_image():
    filename = tk.filedialog.asksaveasfilename(title="Save Image", filetypes=(("png files", "*.png"),))

    if filename[:-4] != ".png":
        filename += ".png"

    fractal_label.image.write(filename, format="png")


# Menu GUI
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Image", command=save_image)
menu_bar.add_cascade(label="File", menu=file_menu)

examples_menu = tk.Menu(menu_bar, tearoff=0)

for ex in examples.all_examples:
    def load_example(example=ex):
        transformations_frame.num_selector_entry.delete(0, tk.END)
        transformations_frame.num_selector_entry.insert(0, example.ifs.size)
        transformations_frame.num_selected()

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

    examples_menu.add_command(label=ex.name, command=load_example)

menu_bar.add_cascade(label="Examples", menu=examples_menu)

root.config(menu=menu_bar)

root.wm_title("IFS Code Visualizer")

root.mainloop()
