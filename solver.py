# Name: solver.py
# Date: Decemeber 19th, 2022
# Coder: Amelia Eric-Markovic
# Creator: techwithtim.net

# Checks if the board has been solved
# bo: Board multidimensional list
def solve(bo):
    # Checks if the 
    find = find_empty(bo)
    # Found the solution
    if not find:
        return True
    # Solution not found
    else:
        row, col = find
    # Checks through all the columns
    for i in range(1,10):
        # Checks if the 
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

# Checks if the new number put in is valid
# bo: Board multidimensional list
# num: Insterted number
# pos: Position of the newly inserted number
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        # Checks if the new number already exists
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        # Checks if the new number already exists
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    # checks for each row by number
    for i in range(box_y * 3, box_y * 3 + 3):
        # Checks the column by number
        for j in range(box_x * 3, box_x * 3 + 3):
            # Checks if the new number already exists
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

# Displays the board
# bo: Board multidimensional list
def print_board(bo):
    # Loops through every row
    for i in range(len(bo)):
        # Checks if the row is the third row and is not the first row
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        # Loops through every column
        for j in range(len(bo[0])):
            # Checks if the column is the third column and is not the first column
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            # Checks if in the last column
            if j == 8:
                print(bo[i][j])
            # Adds spaces between numbers if not the last column
            else:
                print(str(bo[i][j]) + " ", end="")

# Checks for an empty square on the board
# bo: Board multidimensional list
def find_empty(bo):
    # Checks through every row
    for i in range(len(bo)):
        # Checks through every column
        for j in range(len(bo[0])):
            # Checks if the square equals 0
            if bo[i][j] == 0:
                return (i, j)  # returns the row, column
    # No empty square was found
    return None