from solver import solve
from kociemba_solver import solve_kociemba
from cube import Cube
from utils import random_scramble
import time
import pycuber as pc

def verify(scramble, solution):
    cube = pc.Cube()
    cube(pc.Formula(scramble.replace("p", "'")))
    cube(pc.Formula(" ".join(solution)))
    return cube == pc.Cube()

def main():
    print("=== Rubik's Cube Solver ===")
    print("Commands:")
    print(" 1 → Solve custom scramble")
    print(" 2 → Generate random scramble")
    print(" exit → Quit\n")

    while True:
        choice = input("Select option: ").strip()

        if choice == "exit":
            break

        elif choice == "1":
            scramble = input("Enter scramble: ").strip()
            start = time.time()
            solution = solve(scramble)
            elapsed = time.time() - start

            print("\nSolution:", " ".join(solution))
            print("Moves:", len(solution))
            print("Time: %.4f seconds" % elapsed)
            print("Verified:", verify(scramble, solution))
            print()

        elif choice == "2":
            scramble = random_scramble()
            print("\nGenerated scramble:")
            print(scramble)

            start = time.time()
            solution = solve(scramble)
            elapsed = time.time() - start

            print("\nSolution:", " ".join(solution))
            print("Moves:", len(solution))
            print("Time: %.4f seconds" % elapsed)
            print("Verified:", verify(scramble, solution))
            print()

        
            

        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    main()
