import kociemba
import pycuber as pc

def solve_kociemba(scramble):
    """
    Universal solver using PyCuber for legality
    and Kociemba for solving.
    """

    # Convert Rp → R'
    scramble = scramble.replace("p", "'")

    # Apply scramble safely
    cube = pc.Cube()
    cube(pc.Formula(scramble))

    # Map colors to face letters using centers
    color_to_face = {}

    face_order = ['U', 'R', 'F', 'D', 'L', 'B']

    # Determine mapping from center colors
    for face in face_order:
        center_color = cube.get_face(face)[1][1].colour
        color_to_face[center_color] = face

    # Build 54-character string
    state = ""

    for face in face_order:
        face_data = cube.get_face(face)
        for row in face_data:
            for square in row:
                state += color_to_face[square.colour]

    return kociemba.solve(state).split()
