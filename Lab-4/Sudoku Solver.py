import time
import copy

# Sample Sudoku puzzle (0 = empty)
puzzle = [
    [8,0,0,0,0,0,0,0,0],
    [0,0,3,6,0,0,0,0,0],
    [0,7,0,0,9,0,2,0,0],
    [0,5,0,0,0,7,0,0,0],
    [0,0,0,0,4,5,7,0,0],
    [0,0,0,1,0,0,0,3,0],
    [0,0,1,0,0,0,0,6,8],
    [0,0,8,5,0,0,0,1,0],
    [0,9,0,0,0,0,4,0,0]
]

# --- Student Task 1: Implement this ---
def is_safe(board, row, col, num):
    """Check if 'num' can be placed at board[row][col]"""
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# --- Student Task 2: Naive backtracking solver ---
naive_calls = 0
def solve_naive(board):
    global naive_calls
    naive_calls += 1
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_naive(board):
                return True
            board[row][col] = 0
    return False

# --- Student Task 3: MRV heuristic solver ---
mrv_calls = 0
def get_possible(board, row, col):
    possible = set(range(1, 10))
    # Remove numbers in row and column
    for i in range(9):
        possible.discard(board[row][i])
        possible.discard(board[i][col])
    # Remove numbers in 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            possible.discard(board[start_row + i][start_col + j])
    return possible

def find_mrv(board):
    min_count = 10
    min_cell = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible = get_possible(board, i, j)
                if len(possible) < min_count:
                    min_count = len(possible)
                    min_cell = (i, j)
                if min_count == 1:
                    return min_cell
    return min_cell

def solve_mrv(board):
    global mrv_calls
    mrv_calls += 1
    empty = find_mrv(board)
    if not empty:
        return True
    row, col = empty
    possible = get_possible(board, row, col)
    for num in possible:
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_mrv(board):
                return True
            board[row][col] = 0
    return False

# --- Student Task 4: MRV + LCV solver ---
mrv_lcv_calls = 0
def count_constraints(board, row, col, num):
    """Count how many choices neighbors lose if 'num' is placed here"""
    count = 0
    # Check row and column
    for i in range(9):
        if board[row][i] == 0 and num in get_possible(board, row, i):
            count += 1
        if board[i][col] == 0 and num in get_possible(board, i, col):
            count += 1
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            r, c = start_row + i, start_col + j
            if board[r][c] == 0 and num in get_possible(board, r, c):
                count += 1
    return count

def solve_mrv_lcv(board):
    global mrv_lcv_calls
    mrv_lcv_calls += 1
    empty = find_mrv(board)
    if not empty:
        return True
    row, col = empty
    possible = list(get_possible(board, row, col))
    # Least Constraining Value: sort by how few constraints they impose
    possible.sort(key=lambda num: count_constraints(board, row, col, num))
    for num in possible:
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_mrv_lcv(board):
                return True
            board[row][col] = 0
    return False

# --- Utility: find empty cell ---
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# --- Runner ---
def run_solver(solver, name):
    board_copy = copy.deepcopy(puzzle)
    start = time.time()
    solver(board_copy)
    end = time.time()
    print(f"{name}: Time = {end-start:.6f}s, Recursive calls = {globals()[name+'_calls']}")
    for row in board_copy:
        print(row)
    print("\n"+"-"*40+"\n")

# --- Execute ---
run_solver(solve_naive, "naive")
run_solver(solve_mrv, "mrv")
run_solver(solve_mrv_lcv, "mrv_lcv")