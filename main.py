# Import the necessary module 'tkinter' for GUI development
from tkinter import *

# Import custom modules 'unit', 'configure', and 'new'
from unit import Cell
import configure
import new

# Create a new Tkinter window
root = Tk()

# Override the window's configuration settings
root.configure(bg="grey")                   # Set background color to grey
root.geometry(f'{configure.WIDTH}x{configure.HEIGHT}')  # Set window dimensions
root.title("Minesweeper Game")              # Set window title
root.resizable(False, False)                # Disable window resizing

# Create a top frame for the title
top_frame = Frame(
    root,
    bg='#5D6D7E',                          # Set background color to a shade of blue
    width=configure.WIDTH,
    height=new.height_prct(25)              # Set the frame's height based on a percentage of the window height
)
top_frame.place(x=0, y=0)                  # Place the frame at coordinates (0, 0) in the window

# Create a label for the game title and place it within the top frame
game_title = Label(
    top_frame,
    bg='#5D6D7E',
    fg='white',                             # Set text color to white
    text='Minesweeper Game',
    font=('', 48)                           # Set font and font size
)
game_title.place(
    x=new.width_prct(30), y=0               # Set label position within the top frame
)

# Create a center frame for the game grid
center_frame = Frame(
    root,
    bg='black',                             # Set background color to black
    width=new.width_prct(75),               # Set the frame's width based on a percentage of the window width
    height=new.height_prct(75)              # Set the frame's height based on a percentage of the window height
)
center_frame.place(
    x=new.width_prct(30),                   # Set the position of the center frame
    y=new.height_prct(30),
)

# Create a grid of cells using a nested loop
for x in range(configure.GRID_SIZE):
    for y in range(configure.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)    # Create a button object for each cell
        c.cell_btn_object.grid(
            column=x, row=y                  # Place the cell button in the grid
        )

# Call the label creation method from the Cell class for displaying mine counts
Cell.create_cell_count_label(top_frame)
Cell.cell_count_label_object.place(
    x=new.width_prct(42),                   # Set the position of the label
    y=new.height_prct(15)
)

# Randomly place mines on the game grid
Cell.randomize_mines()

# Start the Tkinter main event loop to display the window
root.mainloop()
