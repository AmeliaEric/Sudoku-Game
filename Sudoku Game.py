# Name: Sudoku Game.py
# Date: Decemeber 19th, 2022
# Coder: Amelia Eric-Markovic
# Creator: techwithtim.net
import pygame
from solver import solve, valid
import time
pygame.font.init()


class Grid:
    # Initialize the grid with a given board configuration
    board = [
        [7,8,0,4,0,0,1,2,0],
        [6,0,0,0,7,5,0,0,9],
        [0,0,0,6,0,1,0,7,8],
        [0,0,7,0,4,0,2,6,0],
        [0,0,1,0,5,0,9,3,0],
        [9,0,4,0,6,0,0,0,5],
        [0,7,0,3,0,0,0,1,2],
        [1,2,0,0,0,7,4,0,0],
        [0,4,9,2,0,6,0,0,7]
    ]


    # Initializes the grid with the specified number of rows, columns, width, and height
    # rows: Number of rows in the grid
    # cols: Number of columns in the grid
    # width: Width of each cube
    # height: Height of each cube
    def __init__(self, rows, cols, width, height):
        # Set the number of rows and columns for the grid
        self.rows = rows
        self.cols = cols
        # Create a 2D list of cubes with the specified dimensions
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        # Set the width and height of each cube
        self.width = width
        self.height = height
        # Set the model to None
        self.model = None
        # Set the selected cube to None
        self.selected = None

    # Update the model with the current values of the cubes
    def update_model(self):
        # Set the model to a 2D list of the values of the cubes
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # Place a value in the selected cube and check if it is a valid move
    # val: Value to place in the selected cube
    def place(self, val):
        # Get the row and column of the selected cube
        row, col = self.selected
        # Check if the selected cube is empty
        if self.cubes[row][col].value == 0:
            # Set the value of the selected cube
            self.cubes[row][col].set(val)
            # Update the model
            self.update_model()
            # Check if the move is valid and the puzzle can be solved with the new value
            if valid(self.model, val, (row,col)) and solve(self.model):
                # Return True if the move is valid and the puzzle can be solved
                return True
            else:
                # If the move is not valid or the puzzle cannot be solved, reset the selected cube and return False
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # Sketch a temporary value in the selected cube
    # val: Value to sketch in the selected cube
    def sketch(self, val):
        # Get the row and column of the selected cube
        row, col = self.selected
        # Set the temporary value of the selected cube
        self.cubes[row][col].set_temp(val)

    # Draw the grid and cubes on the window
    # win: Window to draw on
    def draw(self, win):
        # Draw the grid lines on the window
        gap = self.width / 9
        for i in range(self.rows+1):
            # Set the thickness of the line
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            # Draw horizontal line
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            # Draw vertical line
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw the cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    # Select a cube and reset all others
    # row: Row of the selected cube
    # col: Column of the selected cube
    def select(self, row, col):
        # Reset the selected status of all cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        # Set the selected status of the chosen cube
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # Clear the temporary value of the selected cube
    def clear(self):
        row, col = self.selected
        # Only clear if the cube has no permanent value
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # Check if the mouse was clicked inside the grid
    # pos: Mouse click position
    # return: Tuple of row and column if inside the grid, None if outside
    def click(self, pos):
        # Check if the mouse click was inside the grid
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            # Return the row and column of the clicked position
            return (int(y),int(x))
        else:
            # Return None if outside the grid
            return None

    # Check if the puzzle is finished
    # return: True if finished, False if not
    def is_finished(self):
        # Check each cube
        for i in range(self.rows):
            for j in range(self.cols):
                # Return False if any cube is empty
                if self.cubes[i][j].value == 0:
                    return False
        # Return True if no empty cubes
        return True

class Cube:
    rows = 9
    cols = 9

    # Initialize a new Cube object
    # value: Value to be displayed on the cube
    # row: Row position of the cube on the board
    # col: Column position of the cube on the board
    # width: Width of the cube
    # height: Height of the cube
    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # Draw the cube on the window
    # win: Window to draw on
    def draw(self, win):
        # Set the font for the value
        fnt = pygame.font.SysFont("comicsans", 40)

        # Calculate the gap between cells
        gap = self.width / 9
        # Calculate the top-left x coordinate of the cell
        x = self.col * gap
        # Calculate the top-left y coordinate of the cell
        y = self.row * gap

        # If the cube has a temporary value and no permanent value, render the temporary value
        if self.temp != 0 and self.value == 0:
            # Render the temporary value in light grey
            text = fnt.render(str(self.temp), 1, (128,128,128))
            # Draw the text on the window with a small offset
            win.blit(text, (x+5, y+5))
        # If the cube has a permanent value, render the permanent value
        elif not(self.value == 0):
            # Render the permanent value in black
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            # Draw the text on the window with the text centered in the cell
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        # If the cube is selected, draw a red border around it
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)


    # Set the permanent value of the cube
    # val: New value for the cube
    def set(self, val):
        self.value = val

    # Set the temporary value of the cube
    # val: New temporary value for the cube
    def set_temp(self, val):
        self.temp = val



# Redraw the window with the updated board and timer
# win: Window to draw on
# board: Board object to draw
# time: Time in seconds to display
# strikes: Number of strikes to display
def redraw_window(win, board, time, strikes):
    # Fill the window with white
    win.fill((255,255,255))

    # Set the font for the text
    fnt = pygame.font.SysFont("comicsans", 40)
    # Render the time text
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    # Draw the time text on the window
    win.blit(text, (540 - 160, 560))
    # Render the strikes text
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    # Draw the strikes text on the window
    win.blit(text, (20, 560))
    # Draw the board on the window
    board.draw(win)


# Format the time as a string in the format HH:MM:SS
# secs: Time in seconds
# return: Formatted time string
def format_time(secs):
    # Calculate the number of seconds
    sec = secs % 60
    # Calculate the number of minutes
    minute = secs // 60
    # Calculate the number of hours
    hour = minute // 60

    # Format the time as a string
    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    # Create the window
    win = pygame.display.set_mode((610,620))
    # Set the window caption
    pygame.display.set_caption("Sudoku")
    # Create the board
    board = Grid(9, 9, 540, 540)
    # Initialize the key variable
    key = None
    # Set the run variable to True to start the game loop
    run = True
    # Record the start time
    start = time.time()
    # Initialize the number of strikes to 0
    strikes = 0

    # Main game loop
    while run:
        # Calculate the elapsed time
        play_time = round(time.time() - start)

        # Handle events
        for event in pygame.event.get():
            # If the user closes the window, set run to False to stop the game loop
            if event.type == pygame.QUIT:
                run = False
            # If the user presses a key
            if event.type == pygame.KEYDOWN:
                # Set the key variable based on the key that was pressed
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                # If the user pressed the Delete key, clear the selected cell
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                # If the user pressed the Return key, try to place the temporary value in the selected cell
                if event.key == pygame.K_RETURN:
                    # Get the indices of the selected cell
                    i, j = board.selected
                    # If the selected cell has a temporary value
                    if board.cubes[i][j].temp != 0:
                        # Try to place the temporary value in the cell
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        # Reset the key variable
                        key = None

                        # If the puzzle is finished, end the game loop
                        if board.is_finished():
                            print("Game over")
                            run = False

            # If the user clicked the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                pos = pygame.mouse.get_pos()
                # Check if the click was on a cell
                clicked = board.click(pos)
                # If a cell was clicked, select it and reset the key variable
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        # If a cell is selected and a key has been pressed, try to sketch the value in the cell
        if board.selected and key is not None:
            board.sketch(key)

        # Redraw the window and update the display
        redraw_window(win, board, play_time, strikes)
        pygame.display.update()
# Run the main game loop
main()

# Quit pygame
pygame.quit()
