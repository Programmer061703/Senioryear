# Initialize a Sudoku grid
sudoku_grid = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

def is_valid_move(board, row, col, num):
    # Check row, column and the 3x3 square
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

# Backtracking Algorithm
def backtracking(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if backtracking(board):
                            return True
                        board[row][col] = 0
                return False
    return True  # Whole board filled correctly

# Forward Checking Algorithm
### YOUR CODE HERE ###
# Implement Forward Checking here
def forward_checking(board):
    pass



### END YOUR CODE ###

# Arc Consistency (AC-3) Algorithm
### YOUR CODE HERE ###
# Implement AC-3 here
def arc_consistency(board):
    pass



### END YOUR CODE ###


# Main function to choose the algorithm
def solve_sudoku(method):
    if method == 'backtracking':
        if backtracking(sudoku_grid):
            print("Solved by Backtracking")
            print(sudoku_grid)
    elif method == 'forward_checking':
        # Call your forward_checking function here
        pass
    elif method == 'arc_consistency':
        # Call your arc_consistency function here
        pass
    else:
        print("Invalid method")

# Example usage
solve_sudoku('backtracking')