import random
import sys
import os

def main():
    
    
    clear_screen()
    game_play()

    
def level():
    while True:
        try:
            n = int(input("Enter Level: "))
            if n > 3 or n < 1:
                raise ValueError
            else:
                if n == 1:
                    return 7
                if n == 2:
                    return 10
                if n == 3:
                    return 13
        except ValueError:
            print("Invalid Input")


def back_grid(n):
    k = 0
    list = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            k += 1
            list[i][j] = k
    return list


def grid_display(n, grid):
    
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

    
def put_bombs(n, list):
    if n == 7:
        k = 7
    elif n == 10:
        k = 16
    elif n == 13:
        k = 35

    bomb_count = 0
    while bomb_count != k:
        bomb = random.randint(1, n ** 2)
        for i in range(n):
            for j in range(n):
                if list[i][j] == bomb:
                    if list[i][j] != "*":
                        list[i][j] = "*"
                        bomb_count += 1
    return k


def make_grid(n, list):
    for i in range(n):
        for j in range(n):
            if list[i][j] != "*":
                list[i][j] = 0

    try:
        for i in range(n):
            for j in range(n):
                count = 0
                if list[i][j] != "*":
                    if i > 0 and list[i - 1][j] == "*":
                        count += 1
                    if i > 0 and j > 0 and list[i - 1][j - 1] == "*":
                        count += 1
                    if i > 0 and j < n - 1 and list[i - 1][j + 1] == "*":
                        count += 1
                    if j > 0 and list[i][j - 1] == "*":
                        count += 1
                    if j < n - 1 and list[i][j + 1] == "*":
                        count += 1
                    if i < n - 1 and list[i + 1][j] == "*":
                        count += 1
                    if i < n - 1 and j > 0 and list[i + 1][j - 1] == "*":
                        count += 1
                    if i < n - 1 and j < n - 1 and list[i + 1][j + 1] == "*":
                        count += 1
                    list[i][j] = count
        return list
    except IndexError:
        pass


def reveal_zeros(n, x, y, inner_grid, outer_grid):
    if x < 0 or x >= n or y < 0 or y >= n:
        return
    if outer_grid[x][y] != "▓":
        return
    if inner_grid[x][y] != 0:
        outer_grid[x][y] = inner_grid[x][y]
        return
    outer_grid[x][y] = inner_grid[x][y]
    reveal_zeros(n, x - 1, y, inner_grid, outer_grid)
    reveal_zeros(n, x + 1, y, inner_grid, outer_grid)
    reveal_zeros(n, x, y - 1, inner_grid, outer_grid)
    reveal_zeros(n, x, y + 1, inner_grid, outer_grid)
    reveal_zeros(n, x + 1, y + 1, inner_grid, outer_grid)
    reveal_zeros(n, x - 1, y + 1, inner_grid, outer_grid)
    reveal_zeros(n, x + 1, y - 1, inner_grid, outer_grid)
    reveal_zeros(n, x - 1, y - 1, inner_grid, outer_grid)
    

def win_matrix(n, inner_grid, outer_grid):
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
    inner_grid = back_grid(n)
    flags = put_bombs(n, inner_grid)

    grid = make_grid(n, inner_grid)
    grid_display(n, outer_grid)

    while True:
        if win_matrix(n, inner_grid, outer_grid):
            print("Congrats you won!!!!!!!")
            print()
            endgame()
            print()

        try:
            do = int(input("1. Pop Cell\n2. Insert Flag\n3. Undo Flag\nChoose: "))
            if do < 1 or do > 3:
                raise ValueError
            elif do == 1:
                x, y = input("Enter Coordinate (x,y): ").split(",")
                x = int(x)
                y = int(y)

                if outer_grid[x][y]=="▲":
                    print("The coordinate is flagged")
                    print()

                else:
                    if inner_grid[x][y] == "*":
                        for i in range(n):
                            for j in range(n):
                                if inner_grid[i][j] == "*":
                                    outer_grid[i][j] = "*"
                        clear_screen()
                        grid_display(n, outer_grid)
                        print("Sorry you lost!")
                        print()
                        endgame()
                        print()

                    elif inner_grid[x][y] != 0:
                        outer_grid[x][y] = inner_grid[x][y]
                        clear_screen()
                        grid_display(n, outer_grid)
                        print()
                        print(f"Flags Left: {flags}")
                        print()

                    elif inner_grid[x][y] == 0:
                        reveal_zeros(n, x, y, inner_grid, outer_grid)
                        clear_screen()
                        grid_display(n, outer_grid)
                        print(f"Flags Left: {flags}")
                        print()

            elif do==3:
                a,b=input("Enter Coordinate to unflag: ").split(",")
                a=int(a)
                b=int(b)
                if outer_grid[a][b]=="▲":
                    outer_grid[a][b]="▓"
                    flags=flags+1
                    clear_screen()
                    grid_display(n, outer_grid)
                    print(f"Flags Left: {flags}")
                    print()

                else:
                    clear_screen()
                    grid_display(n, outer_grid)
                    print(f"Flags Left: {flags}")
                    print()
                    print("The coordinate is not flagged")

            else:
                a, b = input("Enter Flag Coordinate (x,y): ").split(",")
                a = int(a)
                b = int(b)
                if outer_grid[a][b] == "▲":
                    print("Already flagged!")
                else:
                    outer_grid[a][b] = "▲"
                    flags -= 1
                clear_screen()
                grid_display(n, outer_grid)
                print(f"Flags Left: {flags}")
                print()

        except ValueError:

            print("Invalid Input")

        except IndexError:
            print("Coordinate out of bounds")


def endgame():
    ans=input("Do you want to play again (Y/N): ").lower()

    if ans=='y':
        game_play()
    elif ans=="n":
        sys.exit()
    else:
        print("invalid input")
        endgame()


if __name__ == "__main__":
    main()

