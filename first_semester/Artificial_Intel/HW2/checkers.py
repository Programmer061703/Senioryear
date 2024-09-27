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
def initialize_domains(board):
    domains = [[set() for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                domains[row][col] = set([board[row][col]])
            else:
                possible_values = set(range(1, 10))
                # Remove values already in the row
                for i in range(9):
                    if board[row][i] != 0:
                        possible_values.discard(board[row][i])
                # Remove values already in the column
                for i in range(9):
                    if board[i][col] != 0:
                        possible_values.discard(board[i][col])
                # Remove values already in the block
                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                for i in range(start_row, start_row + 3):
                    for j in range(start_col, start_col + 3):
                        if board[i][j] != 0:
                            possible_values.discard(board[i][j])
                domains[row][col] = possible_values
    return domains

def forward_checking_helper(board, domains):
    # Check if assignment is complete
    is_complete = True
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                is_complete = False
                break
        if not is_complete:
            break
    if is_complete:
        return True

    # Select unassigned variable with the smallest domain
    min_domain_size = 10
    min_row, min_col = -1, -1
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domain_size = len(domains[row][col])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    min_row, min_col = row, col
    if min_domain_size == 0:
        return False  # Failure due to empty domain

    # For each value in the domain
    for value in domains[min_row][min_col].copy():
        # Try assigning the value
        board[min_row][min_col] = value
        # Keep track of changes to domains
        changes = []
        success = True
        # Remove 'value' from the domains of variables in the same row, column, block
        # Row
        for col in range(9):
            if col != min_col and board[min_row][col] == 0:
                if value in domains[min_row][col]:
                    changes.append((min_row, col, domains[min_row][col].copy()))
                    domains[min_row][col].discard(value)
                    if len(domains[min_row][col]) == 0:
                        success = False
        # Column
        for row in range(9):
            if row != min_row and board[row][min_col] == 0:
                if value in domains[row][min_col]:
                    changes.append((row, min_col, domains[row][min_col].copy()))
                    domains[row][min_col].discard(value)
                    if len(domains[row][min_col]) == 0:
                        success = False
        # Block
        start_row, start_col = 3 * (min_row // 3), 3 * (min_col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i != min_row or j != min_col) and board[i][j] == 0:
                    if value in domains[i][j]:
                        changes.append((i, j, domains[i][j].copy()))
                        domains[i][j].discard(value)
                        if len(domains[i][j]) == 0:
                            success = False
        if success:
            # Proceed recursively
            result = forward_checking_helper(board, domains)
            if result:
                return True
        # Undo assignment and restore domains
        board[min_row][min_col] = 0
        for row_, col_, domain_ in changes:
            domains[row_][col_] = domain_
    return False  # No value led to a solution

def forward_checking(board):
    domains = initialize_domains(board)
    if forward_checking_helper(board, domains):
        return True
    else:
        return False



def build_neighbors():
    neighbors = {}
    for row in range(9):
        for col in range(9):
            var = (row, col)
            var_neighbors = set()
            # Row neighbors
            for c in range(9):
                if c != col:
                    var_neighbors.add((row, c))
            # Column neighbors
            for r in range(9):
                if r != row:
                    var_neighbors.add((r, col))
            # Block neighbors
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if (i != row or j != col):
                        var_neighbors.add((i, j))
            neighbors[var] = var_neighbors
    return neighbors

def initialize_queue(neighbors):
    queue = []
    for Xi in neighbors:
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))
    return queue

def Revise(domains, Xi, Xj):
    revised = False
    for x in domains[Xi].copy():
        if not any(x != y for y in domains[Xj]):
            domains[Xi].remove(x)
            revised = True
    return revised

def AC3(domains, neighbors):
    queue = initialize_queue(neighbors)
    while queue:
        (Xi, Xj) = queue.pop(0)
        if Revise(domains, Xi, Xj):
            if len(domains[Xi]) == 0:
                return False
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def arc_consistency(board):
    # Initialize domains
    domains = {}
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                domains[(row, col)] = set([board[row][col]])
            else:
                domains[(row, col)] = set(range(1, 10))
    # Build neighbors
    neighbors = build_neighbors()
    # Enforce arc consistency
    result = AC3(domains, neighbors)
    if not result:
        return False
    # Assign singleton domains
    for row in range(9):
        for col in range(9):
            if len(domains[(row, col)]) == 1:
                board[row][col] = next(iter(domains[(row, col)]))
            else:
                board[row][col] = 0
    # Check if assignment is complete
    if all(board[row][col] != 0 for row in range(9) for col in range(9)):
        return True
    else:
        # Proceed with forward checking
        # Convert domains back to list of lists
        domains_list = [[set() for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                domains_list[row][col] = domains[(row, col)]
        if forward_checking_helper(board, domains_list):
            return True
        else:
            return False


# Main function to choose the algorithm
def solve_sudoku(method):
    if method == 'backtracking':
        if backtracking(sudoku_grid):
            print("Solved by Backtracking")
            print(sudoku_grid)
    elif method == 'forward_checking':
        if forward_checking(sudoku_grid):
            print("Solved by Forward Checking")
            print(sudoku_grid)
        else:
            print("No solution found using Forward Checking")
    elif method == 'arc_consistency':
        if arc_consistency(sudoku_grid):
            print("Solved by Arc Consistency")
            print(sudoku_grid)
        else:
            print("No solution found using Arc Consistency")
    else:
        print("Invalid method")

# Example usage
solve_sudoku('forward_checking')
