# Import necessary modules
from tkinter import Button, Label
import random
import configure
import ctypes
import sys

# Define a class called "Cell" for each cell in the Minesweeper grid
class Cell:
    # Class-level variables to keep track of all cells, total cell count, and a label object
    all = []
    cell_count = configure.CELL_COUNT
    cell_count_label_object = None

    # Constructor to initialize a cell
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    # Method to create a button object for the cell
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)  # Bind left-click event
        btn.bind('<Button-3>', self.right_click_actions)  # Bind right-click event
        self.cell_btn_object = btn

    # Static method to create a label for displaying the remaining cell count
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='#5D6D7E',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    # Method to handle left-click actions on a cell
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # Check if the player has won (all non-mine cells are opened)
            if Cell.cell_count == configure.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Over', 0)

        # Cancel left and right-click events if the cell is already opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    # Method to retrieve a cell object based on its coordinates (x, y)
    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    # Property to get a list of cells surrounding the current cell
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    # Property to get the count of mines in surrounding cells
    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    # Method to reveal the content of a cell
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Update the cell count label with the new count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this cell was a mine candidate, set its background color to SystemButtonFace
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )

        # Mark the cell as opened (place this as the last line of the method)
        self.is_opened = True

    # Method to reveal a mine cell
    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()

    # Static method to randomly place mines on the grid
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, configure.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    # Custom string representation for a cell
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
