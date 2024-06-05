import random
import sys
import os

def main():
    clear_screen()
    game_play()

def level():
    # Taking acceptable level input
    while True:
        try:
            n = int(input("Enter Level (1, 2, or 3): "))
            if n == 1:
                return 7
            elif n == 2:
                return 10
            elif n == 3:
                return 13
            else:
                raise ValueError
        except ValueError:
            print("Invalid Input. Please enter a level between 1 and 3.")

def create_grid(n):
    # Create a grid with sequential numbers
    k = 0
    grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            k += 1
            grid[i][j] = k
    return grid

def display_grid(n, grid):
    # Print the column headers (top)
    print("   ", end="")
    for col in range(n):
        print(f"{col:>3}", end=" ")
    print()

    # Print the grid with row headers (left)
    for row in range(n):
        print(f"{row:>2} ", end="")  # Print the row header (left)
        for cell in grid[row]:
            print(f"{str(cell):>3}", end=" ")
        print()
        print()  # Add space between rows

    print()

def place_bombs(n, grid):
    if n == 7:
        bomb_count = 7
    elif n == 10:
        bomb_count = 16
    elif n == 13:
        bomb_count = 35

    placed_bombs = 0
    while placed_bombs < bomb_count:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if grid[i][j] != "*":
            grid[i][j] = "*"
            placed_bombs += 1
    return bomb_count

def generate_numbers(n, grid):
    for i in range(n):
        for j in range(n):
            if grid[i][j] != "*":
                count = 0
                # Check all adjacent cells for bombs
                for x in range(max(0, i-1), min(n, i+2)):
                    for y in range(max(0, j-1), min(n, j+2)):
                        if grid[x][y] == "*":
                            count += 1
                grid[i][j] = count
    return grid

def reveal_zeros(n, x, y, inner_grid, outer_grid):
    if x < 0 or x >= n or y < 0 or y >= n:
        return
    if outer_grid[x][y] != "▓":
        return
    if inner_grid[x][y] != 0:
        outer_grid[x][y] = inner_grid[x][y]
        return
    outer_grid[x][y] = inner_grid[x][y]
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                reveal_zeros(n, x + dx, y + dy, inner_grid, outer_grid)

def check_win(n, inner_grid, outer_grid):
    for i in range(n):
        for j in range(n):
            if inner_grid[i][j] != "*" and outer_grid[i][j] == "▓":
                return False
    return True

def clear_screen():
    os.system('clear') if os.name == 'posix' else os.system('cls')

def game_play():
    print("Hello, Welcome to Minesweeper")
    print("Levels are\n1. 7x7 grid\n2. 10x10 grid\n3. 13x13 grid")
    
    # Taking level input from the user
    n = level()
    outer_grid = [["▓"] * n for _ in range(n)]
    inner_grid = create_grid(n)
    flags = place_bombs(n, inner_grid)

    inner_grid = generate_numbers(n, inner_grid)
    display_grid(n, outer_grid)

    while True:
        if check_win(n, inner_grid, outer_grid):
            print("Congrats you won!!!!!!!")
            print()
            endgame()
            break

        try:
            action = int(input("1. Pop Cell\n2. Insert Flag\n3. Undo Flag\nChoose: "))
            if action < 1 or action > 3:
                raise ValueError
            elif action == 1:
                x, y = map(int, input("Enter Coordinate (x,y): ").split(","))
                if outer_grid[x][y] == "▲":
                    print("The coordinate is flagged")
                else:
                    if inner_grid[x][y] == "*":
                        for i in range(n):
                            for j in range(n):
                                if inner_grid[i][j] == "*":
                                    outer_grid[i][j] = "*"
                        clear_screen()
                        display_grid(n, outer_grid)
                        print("Sorry you lost!")
                        endgame()
                        break
                    elif inner_grid[x][y] == 0:
                        reveal_zeros(n, x, y, inner_grid, outer_grid)
                    else:
                        outer_grid[x][y] = inner_grid[x][y]
                    clear_screen()
                    display_grid(n, outer_grid)
                    print(f"Flags Left: {flags}")
            elif action == 2:
                a, b = map(int, input("Enter Flag Coordinate (x,y): ").split(","))
                if outer_grid[a][b] == "▲":
                    print("Already flagged!")
                else:
                    outer_grid[a][b] = "▲"
                    flags -= 1
                clear_screen()
                display_grid(n, outer_grid)
                print(f"Flags Left: {flags}")
            elif action == 3:
                a, b = map(int, input("Enter Coordinate to unflag (x,y): ").split(","))
                if outer_grid[a][b] == "▲":
                    outer_grid[a][b] = "▓"
                    flags += 1
                else:
                    print("The coordinate is not flagged")
                clear_screen()
                display_grid(n, outer_grid)
                print(f"Flags Left: {flags}")

        except ValueError:
            print("Invalid Input. Please enter valid coordinates and choices.")
        except IndexError:
            print("Coordinate out of bounds. Please enter values within the grid size.")

def endgame():
    ans = input("Do you want to play again (Y/N): ").lower()
    if ans == 'y':
        game_play()
    elif ans == 'n':
        sys.exit()
    else:
        print("Invalid input")
        endgame()

if __name__ == "__main__":
    main()


