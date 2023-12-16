import tkinter as tk
from tkinter import messagebox

# Define colors for different node types
START_COLOR = "green"
GOAL_COLOR = "red"
OBSTACLE_COLOR = "black"
EMPTY_COLOR = "white"

# Define heuristic function (Manhattan distance)
def heuristic(cell1, cell2):
    row1, col1 = cell1
    row2, col2 = cell2
    return abs(row1 - row2) + abs(col1 - col2)

# Class to represent a cell in the grid
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.type = EMPTY_COLOR
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.parent = None

# Initialize the GUI
root = tk.Tk()
root.title("A* Pathfinding Visualization")

# Prompt user for grid dimensions
rows, cols = 50,50 # map(int, input("Enter grid dimensions (rows, columns): ").split())

# Create a 2D array to store cells
grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

# Initialize start and goal cells
start_cell = None
goal_cell = None

# Define cell size based on grid dimensions
cell_size = 400 / cols

# Create a canvas for drawing the grid
canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(padx=5, pady=5)

# Global variable to store the path for visualization
path_to_visualize = []

# Function to draw the grid
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            x, y = col * cell_size, row * cell_size
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=cell.type)

# Function to handle mouse clicks
def on_click(event):
    global start_cell, goal_cell
    col = int(event.x / cell_size)
    row = int(event.y / cell_size)
    cell = grid[row][col]

    # Set start cell if not already set
    if not start_cell and cell.type == EMPTY_COLOR:
        cell.type = START_COLOR
        start_cell = cell
        draw_grid()  # Redraw to show the selected start cell
        prompt_goal()
    # Set goal cell if not already set
    elif not goal_cell and cell.type == EMPTY_COLOR:
        cell.type = GOAL_COLOR
        goal_cell = cell
    # Toggle obstacles
    elif cell.type == EMPTY_COLOR:
        cell.type = OBSTACLE_COLOR
    elif cell.type == OBSTACLE_COLOR:
        cell.type = EMPTY_COLOR

    # Redraw the grid
    draw_grid()

# Prompt user to set goal cell
def prompt_goal():
    messagebox.showinfo("Set Goal", "Click on the cell you want to set as the goal.")

# Function to find neighboring cells
def get_neighbors(cell):
    neighbors = []
    for row_offset, col_offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        new_row = cell.row + row_offset
        new_col = cell.col + col_offset
        if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col].type != OBSTACLE_COLOR:
            neighbors.append(grid[new_row][new_col])
    return neighbors

# Function to find the shortest path using A* algorithm
def find_path():
    # Open set (cells to explore)
    open_set = {start_cell}

    # Closed set (cells already explored)
    closed_set = set()

    # Set g_score of start cell to 0
    start_cell.g_score = 0

    # Show a message to indicate the algorithm is running
    messagebox.showinfo("Algorithm Running", "Finding the shortest path...")

    # Loop until open set is empty or goal is reached
    while open_set:
        # Find the cell with the lowest f_score in the open set
        current_cell = min(open_set, key=lambda cell: cell.f_score)

        # Check if the goal is reached
        if current_cell == goal_cell:
            reconstruct_path()
            return

        # Move current cell from open to closed set
        open_set.remove(current_cell)
        closed_set.add(current_cell)

        # Explore neighbors
        for neighbor in get_neighbors(current_cell):
            if neighbor in closed_set:
                continue  # Skip already explored neighbors

            tentative_g_score = current_cell.g_score + 1  # Assuming a constant cost of movement

            if tentative_g_score < neighbor.g_score:
                neighbor.parent = current_cell
                neighbor.g_score = tentative_g_score
                neighbor.f_score = tentative_g_score + heuristic((neighbor.row, neighbor.col), (goal_cell.row, goal_cell.col))

                if neighbor not in open_set:
                    open_set.add(neighbor)

        # Redraw the grid to visualize the algorithm's progress
        draw_grid()
        canvas.update()
        canvas.after(100)  # Adjust the delay duration as needed

# Function to reconstruct and visualize the shortest path
def reconstruct_path():
    global path_to_visualize
    current_cell = goal_cell
    path_to_visualize = []

    while current_cell != start_cell:
        path_to_visualize.append(current_cell)
        current_cell = current_cell.parent

    # Reverse the path to start from the beginning
    path_to_visualize.reverse()

    # Start visualizing the path
    visualize_path()

# Function to visualize the path with a delay
def visualize_path():
    global path_to_visualize
    if path_to_visualize:
        cell = path_to_visualize.pop(0)
        cell.type = "blue"  # Change the path color
        draw_grid()
        canvas.update()
        canvas.after(200)  # Adjust the delay duration as needed
        visualize_path()
    else:
        # The path visualization is complete
        replay_btn["state"] = tk.NORMAL  # Enable the replay button
        messagebox.showinfo("Simulation Complete", "Shortest path visualization complete!")

# Bind mouse clicks to actions
canvas.bind("<Button-1>", on_click)

# Add a button to start the A* algorithm
start_btn = tk.Button(root, text="Start A* Algorithm", command=find_path)
start_btn.grid(row=1, column=0, columnspan=cols)

# Add a button to replay the simulation (initially disabled)
replay_btn = tk.Button(root, text="Replay Simulation", command=reconstruct_path, state=tk.DISABLED)
replay_btn.grid(row=2, column=0, columnspan=cols)

# Draw the initial grid
draw_grid()

# Run the GUI
root.mainloop()
