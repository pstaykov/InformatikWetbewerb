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

# check columns and rows for full
while 0 in grid:
    recent_grid = grid.copy()
    if np.array_equal(recent_grid, grid):
        for i in range(size):
            for j in range(size):
                if grid[i, j] == 0:
                    grid[i, j] = 1

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


    # check blue diagonals for only 1 needed
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

    # show grid
    plt.imshow(grid, cmap="gray", interpolation="nearest")
    plt.show()
