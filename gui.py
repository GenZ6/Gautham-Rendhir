import tkinter as tk
from tkinter import ttk
import time
import pycuber as pc

from kociemba_solver import solve_kociemba
from utils import random_scramble


COLOR_MAP = {
    "white": "white",
    "yellow": "yellow",
    "red": "red",
    "green": "green",
    "orange": "orange",
    "blue": "blue"
}


def verify(scramble, solution):
    cube = pc.Cube()

    cube(pc.Formula(scramble.replace("p", "'")))
    cube(pc.Formula(" ".join(solution)))

    return cube == pc.Cube()


class CubeSolverGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Rubik's Cube Solver")

        frame = ttk.Frame(root, padding=10)
        frame.pack()

        # Scramble input
        ttk.Label(frame, text="Scramble").pack()

        self.scramble_entry = tk.Entry(frame, width=60)
        self.scramble_entry.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=5)

        ttk.Button(
            button_frame,
            text="Random Scramble",
            command=self.generate_scramble
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Solve",
            command=self.solve_cube
        ).pack(side=tk.LEFT, padx=5)

        # Solution box
        ttk.Label(frame, text="Solution").pack()

        self.solution_box = tk.Text(frame, height=3, width=60)
        self.solution_box.pack(pady=5)

        # Stats
        self.stats_label = ttk.Label(frame, text="")
        self.stats_label.pack(pady=5)

        # Canvas section
        canvas_frame = ttk.Frame(frame)
        canvas_frame.pack(pady=10)

        ttk.Label(canvas_frame, text="Scrambled Cube").grid(row=0, column=0)
        ttk.Label(canvas_frame, text="Solved Cube").grid(row=0, column=1)

        self.scramble_canvas = tk.Canvas(canvas_frame, width=300, height=220, bg="white")
        self.scramble_canvas.grid(row=1, column=0, padx=10)

        self.solve_canvas = tk.Canvas(canvas_frame, width=300, height=220, bg="white")
        self.solve_canvas.grid(row=1, column=1, padx=10)

    def generate_scramble(self):

        scramble = random_scramble()
        self.scramble_entry.delete(0, tk.END)
        self.scramble_entry.insert(0, scramble)

    def solve_cube(self):

        scramble = self.scramble_entry.get()

        if not scramble:
            self.stats_label.config(text="Please enter scramble")
            return

        start = time.time()

        try:
            solution = solve_kociemba(scramble)

            if isinstance(solution, str):
                solution = solution.split()

            elapsed = time.time() - start

            self.solution_box.delete("1.0", tk.END)
            self.solution_box.insert(tk.END, " ".join(solution))

            # Scrambled cube
            scrambled_cube = pc.Cube()
            scrambled_cube(pc.Formula(scramble.replace("p", "'")))

            self.draw_cube(scrambled_cube, self.scramble_canvas)

            # Solved cube
            solved_cube = pc.Cube()
            solved_cube(pc.Formula(scramble.replace("p", "'")))
            solved_cube(pc.Formula(" ".join(solution)))

            self.draw_cube(solved_cube, self.solve_canvas)

            verified = verify(scramble, solution)

            self.stats_label.config(
                text=f"Moves: {len(solution)} | Time: {elapsed:.4f}s | Solved: {verified}"
            )

        except Exception as e:
            self.stats_label.config(text=f"Error: {e}")

    def draw_cube(self, cube, canvas):

        canvas.delete("all")

        size = 25
        start_x = 100
        start_y = 20

        faces = ["U", "L", "F", "R", "B", "D"]

        positions = {
            "U": (start_x, start_y),
            "L": (start_x - 75, start_y + 75),
            "F": (start_x, start_y + 75),
            "R": (start_x + 75, start_y + 75),
            "B": (start_x + 150, start_y + 75),
            "D": (start_x, start_y + 150)
        }

        for face in faces:

            x0, y0 = positions[face]
            face_colors = cube.get_face(face)

            for i in range(3):
                for j in range(3):

                    sticker = face_colors[i][j].colour
                    color = COLOR_MAP.get(sticker, "gray")

                    x = x0 + j * size
                    y = y0 + i * size

                    canvas.create_rectangle(
                        x,
                        y,
                        x + size,
                        y + size,
                        fill=color,
                        outline="black"
                    )


if __name__ == "__main__":

    root = tk.Tk()
    app = CubeSolverGUI(root)
    root.mainloop()
