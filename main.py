import random
import sys
import os

def main():
    print("Hello, Welcome to Minesweeper")
    print("Levels are\n1. 7x7 grid\n2. 10x10 grid\n3. 13x13 grid")
    
    # Taking level input from the user
    n = level()
    list_out = [["▓"] * n for _ in range(n)]
    list_in = back_grid(n)
    flags = put_bombs(n, list_in)

    grid = make_grid(n, list_in)
    grid_display(n, list_out)

    while True:
        if win_matrix(n, list_in, list_out):
            sys.exit("Congrats you won!!!!!!!")

        try:
            do = int(input("1. Pop Cell\n2. Insert Flag\nChoose: "))
            if do < 1 or do > 2:
                raise ValueError
            elif do == 1:
                x, y = input("Enter Coordinate (x,y): ").split(",")
                x = int(x)
                y = int(y)
                if list_in[x][y] == "*":
                    for i in range(n):
                        for j in range(n):
                            if list_in[i][j] == "*":
                                list_out[i][j] = "*"
                    clear_screen()
                    grid_display(n, list_out)
                    sys.exit("Sorry you lost!")

                elif list_in[x][y] != 0:
                    list_out[x][y] = list_in[x][y]
                    clear_screen()
                    grid_display(n, list_out)
                    print()
                    print(f"Flags Left: {flags}")
                    print()

                elif list_in[x][y] == 0:
                    reveal_zeros(n, x, y, list_in, list_out)
                    clear_screen()
                    grid_display(n, list_out)
                    print(f"Flags Left: {flags}")
                    print()

            else:
                a, b = input("Enter Flag Coordinate (x,y): ").split(",")
                a = int(a)
                b = int(b)
                if list_out[a][b] == "F":
                    print("Already flagged!")
                else:
                    list_out[a][b] = "F"
                    flags -= 1
                clear_screen()
                grid_display(n, list_out)
                print(f"Flags Left: {flags}")
                print()

        except ValueError:
            print("Invalid Input")

        except IndexError:
            print("Coordinate out of bounds")


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
    for row in grid:
        print()
        for cell in row:
            print(f"{str(cell):>3}", end=" ")
            
        print()
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


def reveal_zeros(n, x, y, list_in, list_out):
    if x < 0 or x >= n or y < 0 or y >= n:
        return
    if list_out[x][y] != "▓":
        return
    if list_in[x][y] != 0:
        list_out[x][y] = list_in[x][y]
        return
    list_out[x][y] = list_in[x][y]
    reveal_zeros(n, x - 1, y, list_in, list_out)
    reveal_zeros(n, x + 1, y, list_in, list_out)
    reveal_zeros(n, x, y - 1, list_in, list_out)
    reveal_zeros(n, x, y + 1, list_in, list_out)
    reveal_zeros(n, x + 1, y + 1, list_in, list_out)
    reveal_zeros(n, x - 1, y + 1, list_in, list_out)
    reveal_zeros(n, x + 1, y - 1, list_in, list_out)
    reveal_zeros(n, x - 1, y - 1, list_in, list_out)
    


def win_matrix(n, list_in, list_out):
    for i in range(n):
        for j in range(n):
            if list_in[i][j] != "*" and list_out[i][j] == "▓":
                return False
    return True


def clear_screen():
    os.system('clear') if os.name == 'posix' else os.system('cls')


if __name__ == "__main__":
    main()

