import numpy as np
import matplotlib.pyplot as plt

def read_tomograph(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    n = int(lines[0])  # Größe n x n
    cols = list(map(int, lines[1].split()))
    rows = list(map(int, lines[2].split()))
    blue_diagonals = list(map(int, lines[3].split()))
    yellow_diagonals = list(map(int, lines[4].split()))
    
    return n, cols, rows, blue_diagonals, yellow_diagonals

size, cols, rows, blue_diagonals, yellow_diagonals = read_tomograph(r"eingaben/tomograph00.txt")

def blue_diagonal_positions(diagonal_index):
    positions = []
    if diagonal_index < size:
        for i in range(diagonal_index + 1):
            positions.append((i, diagonal_index-i))
    else:
        for i in range(2*size - diagonal_index - 1):
            positions.append((size - i - 1, diagonal_index - size + i + 1))
    return positions

def yellow_diagonal_positions(diagonal_index):
    positions = []
    if diagonal_index < size:
        for i in range(diagonal_index + 1):
            positions.append((size - diagonal_index + i - 1, i))
    else:
        for i in range(2 * size - diagonal_index - 1):
            positions.append((i, diagonal_index - size + i + 1))
    return positions

grid = np.zeros((size, size), dtype=int)

# ----------Initial marking based on 0 counts---------- (yes i do comment like this this was not chatgpt)
# check columns and rows for 0
def check_initial_zeros(grid):
    for j, col in enumerate(cols):  
        if col == 0:
            grid[:, j] = -1  

    for i, row in enumerate(rows):
        if row == 0:
            grid[i, :] = -1

    # check diagonals for 0
    for d, diagonal in enumerate(blue_diagonals):
        if diagonal == 0:
            for i, j in blue_diagonal_positions(d):
                grid[i, j] = -1
    for d, diagonal in enumerate(yellow_diagonals):
        if diagonal == 0:
            for i, j in yellow_diagonal_positions(d):
                grid[i, j] = -1 

# ----------moves by the marks----------
def move_by_marks(grid):
    # check columns and rows 

    for i, col in enumerate(cols):  
        filled = np.sum(grid[:, i] == 1)
        blocked = np.sum(grid[:, i] == -1)
        if filled == col:
            grid[grid[:, i] == 0, i] = -1
        elif blocked == size - col:
            grid[grid[:, i] == 0, i] = 1

    for j, row in enumerate(rows):  
        filled = np.sum(grid[j, :] == 1)
        blocked = np.sum(grid[j, :] == -1)
        if filled == row:
            grid[j, grid[j, :] == 0] = -1
        elif blocked == size - row:
            grid[j, grid[j, :] == 0] = 1


    # check blue diagonals 
    for d, diagonal in enumerate(blue_diagonals):
        size_of_diagonal = d + 1 if d < size else 2 * size - d - 1
        positions = blue_diagonal_positions(d)
        
        # Count filled and blocked cells
        filled = np.sum([grid[i, j] == 1 for i, j in positions])
        blocked = np.sum([grid[i, j] == -1 for i, j in positions])
        
        # If we already have enough filled cells, block the rest
        if filled == diagonal:
            for pos in positions:
                if grid[pos] == 0:
                    grid[pos] = -1
        
        # If we have enough blocked cells, fill the rest
        elif blocked == size_of_diagonal - diagonal:
            for pos in positions:
                if grid[pos] == 0:
                    grid[pos] = 1

    # check yellow diagonals 
    for d, diagonal in enumerate(yellow_diagonals):
        size_of_diagonal = d + 1 if d < size else 2 * size - d - 1
        positions = yellow_diagonal_positions(d)
        
        # Count filled and blocked cells
        filled = np.sum([grid[i, j] == 1 for i, j in positions])
        blocked = np.sum([grid[i, j] == -1 for i, j in positions])
        
        # If we already have enough filled cells, block the rest
        if filled == diagonal:
            for pos in positions:
                if grid[pos] == 0:
                    grid[pos] = -1
        
        # If we have enough blocked cells, fill the rest
        elif blocked == size_of_diagonal - diagonal:
            for pos in positions:
                if grid[pos] == 0:
                    grid[pos] = 1

# ----------check if grid is valid----------
def is_grid_valid(grid):
    # check columns and rows
    for i, col in enumerate(cols):
        if np.sum(grid[:, i] == 1) > col:
            return False
    for j, row in enumerate(rows):
        if np.sum(grid[j, :] == 1) > row:
            return False

    # check blue diagonals
    for d, diagonal in enumerate(blue_diagonals):
        positions = blue_diagonal_positions(d)
        if np.sum([grid[i, j] == 1 for i, j in positions]) > diagonal:
            return False

    # check yellow diagonals
    for d, diagonal in enumerate(yellow_diagonals):
        positions = yellow_diagonal_positions(d)
        if np.sum([grid[i, j] == 1 for i, j in positions]) > diagonal:
            return False

    return True

def is_grid_complete(grid):
    for i, col in enumerate(cols):
        if np.sum(grid[:, i] == 1) != col:
            return False
    for j, row in enumerate(rows):
        if np.sum(grid[j, :] == 1) != row:
            return False
    for d, diagonal in enumerate(blue_diagonals):
        positions = blue_diagonal_positions(d)
        if np.sum([grid[i, j] == 1 for i, j in positions]) != diagonal:
            return False
    for d, diagonal in enumerate(yellow_diagonals):
        positions = yellow_diagonal_positions(d)
        if np.sum([grid[i, j] == 1 for i, j in positions]) != diagonal:
            return False
    return True

# recursion to solve the grid
def solve_grid(grid):
    if is_grid_complete(grid):
        return grid
        
    current_grid = grid.copy()
    move_by_marks(current_grid)

    if np.array_equal(current_grid, grid):        
        empty_cells = np.argwhere(grid == 0)
        if len(empty_cells) > 0:
            i, j = empty_cells[0]
            guess_grid = grid.copy()

            guess_grid[i, j] = 1 # try filling

            if is_grid_valid(guess_grid):
                result = solve_grid(guess_grid)
                if result is not False:
                    return result
            
            guess_grid[i, j] = -1 # try blocking

            if is_grid_valid(guess_grid):
                result = solve_grid(guess_grid)
                if result is not False:
                    return result
    else:
        result = solve_grid(current_grid)
        if result is not False:
            return result
    return False

if __name__ == "__main__":
    check_initial_zeros(grid)
    solved_grid = solve_grid(grid)
    if solved_grid is not False:
        grid = solved_grid
    else:
        print("No solution found")


# show grid
plt.imshow(grid, cmap="gray", interpolation="nearest")
plt.show()
