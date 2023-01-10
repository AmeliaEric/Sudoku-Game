# Name: solver.py
# Date: Decemeber 19th, 2022
# Coder: Amelia Eric-Markovic
# Creator: techwithtim.net

# Check if the board has been solved
# bo: Board multidimensional list
def solve(bo):
    # Find an empty cell on the board
    find = find_empty(bo)
    # If no empty cells are found, the solution has been found
    if not find:
        return True
    # If an empty cell is found, try filling it with a valid value
    else:
        row, col = find
    # Try filling the cell with all possible values (1-9)
    for i in range(1,10):
        # Check if the value is valid for the current cell
        if valid(bo, i, (row, col)):
            # Place the value in the cell
            bo[row][col] = i
            # Recursively try to solve the rest of the board with the new value placed
            if solve(bo):
                return True
            # If the value doesn't lead to a solution, reset the cell to empty
            bo[row][col] = 0

    return False


# Check if the newly inserted number is valid
# bo: Board multidimensional list
# num: Inserted number
# pos: Position of the newly inserted number
def valid(bo, num, pos):
    # Check the row for any occurrences of the number
    for i in range(len(bo[0])):
        # If the number exists in the row and it's not in the current cell, return False
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check the column for any occurrences of the number
    for i in range(len(bo)):
        # If the number exists in the column and it's not in the current cell, return False
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Find the box that the current cell is in
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    # Check the box for any occurrences of the number
    # Check each row in the box
    for i in range(box_y * 3, box_y * 3 + 3):
        # Check each column in the box
        for j in range(box_x * 3, box_x * 3 + 3):
            # If the number exists in the box and it's not in the current cell, return False
            if bo[i][j] == num and (i,j) != pos:
                return False

    # If the number is not found in the row, column, or box, return True
    return True


# Displays the board
# bo: Board multidimensional list
def print_board(bo):
    # Loops through every row
    for i in range(len(bo)):
        # If at the third row (and not the first row), print a line to separate the 3x3 squares
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        # Loops through each column of the board
        for j in range(len(bo[0])):
            # If at the third column (and not the first column), print a vertical separator
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            # If at the last column, print the value and move to the next line
            if j == 8:
                print(bo[i][j])
            # If not at the last column, print the value with a space after it
            else:
                print(str(bo[i][j]) + " ", end="")

# Checks for an empty square on the board
# bo: Board multidimensional list
def find_empty(bo):
    # Loops through every row
    for i in range(len(bo)):
        # Loops through every column
        for j in range(len(bo[0])):
            # Returns the position of the empty square if found
            if bo[i][j] == 0:
                return (i, j)  # returns the row, column
    # No empty squares were found
    return None