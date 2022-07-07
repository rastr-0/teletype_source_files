def find_empty_cell(puzzle, l_vars):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                l_vars[0], l_vars[1] = i, j
                return True
    return False

def used_row(puzzle, row, num):
    for i in range(9):
        if puzzle[row][i] == num:
            return True
    return False
    
def used_col(puzzle, col, num):
    for i in range(9):
        if puzzle[i][col] == num:
            return True
    return False
    
def used_box(puzzle, row, col, num):
    for i in range(3):
        for j in range(3):
            if puzzle[i + row][j + col] == num:
                return True
    return False
    
def is_safe(puzzle, row, col, num):
    return not used_row(puzzle, row, num) and not used_col(puzzle, col, num) and not used_box(puzzle, row - row % 3, col - col % 3, num)

def solve_sudoku(puzzle):
    l_vars = [0, 0]
    if not find_empty_cell(puzzle, l_vars):
        return True
        
    row, col = l_vars[0], l_vars[1]
    
    for num in range(1, 10):
        if is_safe(puzzle, row, col, num):
            puzzle[row][col] = num
            if solve_sudoku(puzzle):
                return True
            puzzle[row][col] = 0
            
    return False