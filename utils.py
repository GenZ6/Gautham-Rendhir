def apply_scramble(cube, scramble):
    for move in scramble.split():
        cube.apply_move(move)
import random

MOVES = ["R","Rp","R2","L","Lp","L2",
         "U","Up","U2","D","Dp","D2",
         "F","Fp","F2","B","Bp","B2"]

def random_scramble(length=25):
    scramble = []
    prev_face = None

    for _ in range(length):
        move = random.choice(MOVES)

        # prevent same-face repetition
        while prev_face and move[0] == prev_face:
            move = random.choice(MOVES)

        scramble.append(move)
        prev_face = move[0]

    return " ".join(scramble)
