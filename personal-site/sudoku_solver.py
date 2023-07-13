import tkinter as tk
# This function takes in a cell (row + column) as parameter, based on it, it returns the square it is located in (0-8)
def correct_square_finder(row, column):
    if(row < 3 and column < 3):
        return 0
    elif(row < 3 and column < 6):
        return 1
    elif(row < 3 and column < 9):
        return 2
    elif(row < 6 and column < 3):
        return 3
    elif(row < 6 and column < 6):
        return 4
    elif(row < 6 and column < 9):
        return 5
    elif(row < 9 and column < 3):
        return 6
    elif(row < 9 and column < 6):
        return 7
    elif(row < 9 and column < 9):
        return 8
    
# Square ranges 0,0 - 2,2; 0,3 - 2,5; 0,6 - 2,8;
#               3,0 - 5,2; 3,3 - 5,5; 3,6 - 5,8; 
#               6,0 - 8,2; 6,3 - 8,5; 6,6 - 8,8; 
# Here we're returning a number between 0 and 8. 0 corresponds with upper left corner square and 8 with bottom right square (this becomes important in the square_contents function!)


# This function takes the value from the previous function and returns cell identifiers of the square we're searching for as list in this format [row1, row2, row3, column1, column2, column3]. 
def square_cells(correct_square):
    match correct_square:
        case 0:
            return [0, 1, 2, 0, 1, 2]
        case 1:
            return [0, 1, 2, 3, 4, 5]
        case 2:
            return [0, 1, 2, 6, 7, 8]
        case 3:
            return [3, 4, 5, 0, 1, 2]
        case 4:
            return [3, 4, 5, 3, 4, 5]
        case 5:
            return [3, 4, 5, 6, 7, 8]
        case 6:
            return [6, 7, 8, 0, 1, 2]
        case 7:
            return [6, 7, 8, 3, 4, 5]
        case 8:
            return [6, 7, 8, 6, 7, 8]
# Square ranges 0,0 - 2,2; 0,3 - 2,5; 0,6 - 2,8;
#               3,0 - 5,2; 3,3 - 5,5; 3,6 - 5,8; 
#               6,0 - 8,2; 6,3 - 8,5; 6,6 - 8,8; 
# This is where the numbering system I made in the previous function matters


# This function returns a list of values that are the numbers that already exist in the current square, similarly like in the row_contents and column_contents functions return list of numbers that are already present in the current row and column respectively
def square_contents(correct_square, sudoku_matrix):
    coordinates = square_cells(correct_square)
    contents = [sudoku_matrix[coordinates[0]] [coordinates[3]], sudoku_matrix[coordinates[0]] [coordinates[4]], sudoku_matrix[coordinates[0]] [coordinates[5]], sudoku_matrix[coordinates[1]] [coordinates[3]], sudoku_matrix[coordinates[1]] [coordinates[4]], sudoku_matrix[coordinates[1]] [coordinates[5]], sudoku_matrix[coordinates[2]] [coordinates[3]], sudoku_matrix[coordinates[2]] [coordinates[4]], sudoku_matrix[coordinates[2]] [coordinates[5]], ]
    
    # This loop removes any zeros - zeros only represent empty fields so we don't need to store those as values present in the square
    contents_zeros_removed = []
    for number in contents:
        if number != 0:
            contents_zeros_removed.append(number)
    return contents_zeros_removed


# This function returns a list of all values (numbers) already present in the current row
def row_contents(row, sudoku_matrix):
    contents = []
    for column in range(len(sudoku_matrix)):
        if(sudoku_matrix[row][column] != 0):
            contents.append(sudoku_matrix[row][column])
    return contents

# This function returns a list of all values (numbers) already present in the current column
def column_contents(column, sudoku_matrix):
    contents = []
    for row in range(len(sudoku_matrix)):
        if(sudoku_matrix[row][column] != 0):
            contents.append(sudoku_matrix[row][column])
    return contents


# This function recieves a cell (row + column) as a parameter and returns a list of all the possible solutions (numbers) for that cell by checking each of the numbers between 1 and 9 against the current row, column and square (if it is not yet present, it means the value is a possible solution = appended to the list which returned at the end of the function).
def cell_possible_solutions(sudoku_matrix, row, column):
    possible_numbers = []
    for option in range(len(sudoku_matrix) + 1):
        if (option != 0) and (option not in column_contents(column, sudoku_matrix)) and (option not in row_contents(row, sudoku_matrix)) and (option not in square_contents(correct_square_finder(row, column), sudoku_matrix)):
                        possible_numbers.append(option)
    return possible_numbers

# This in essence returns solutions present in the first list that are not present in the second list
def cell_possible_solutions_comparison(solutions_list1, solutions_list2):
    return list(set(solutions_list2) - set(solutions_list1))


# This function iterates through the whole sudoku_matrix and each time there is a cell that has only one possible solution, it updates the matrix with that solution inputed. At the end the function returns the updated matrix
def cell_has_one_possible_solution(sudoku_matrix):
    for row in range(len(sudoku_matrix)):
        for column in range(len(sudoku_matrix)):
            if sudoku_matrix[row][column] == 0:
                if len(cell_possible_solutions(sudoku_matrix, row, column)) == 1:
                    sudoku_matrix[row][column] = cell_possible_solutions(sudoku_matrix, row, column)[0]
    return sudoku_matrix


# This function returns list of possible solutions in each cell in the row besides the cell selected. This will be used in the next function
def row_possible_solutions_besides_selected_cell(sudoku_matrix, row, column):
    unique_solutions = cell_possible_solutions(sudoku_matrix, row, column)
    solutions = []
    for x in range(len(sudoku_matrix)):
        if sudoku_matrix[row][x] == 0 and x != column:
            solutions += cell_possible_solutions(sudoku_matrix, row, x)
    for number in solutions:
        if number in unique_solutions:
            unique_solutions.remove(number)
    return unique_solutions
    

# This function checks for possible solution for the current cell, if one of those numbers is present only in that specific cell out of the whole row, it places it into the cell and updates the sudoku matrix (then returns it after going through it once)
def cell_has_solution_that_no_other_cell_has_in_row(sudoku_matrix):
    for row in range(len(sudoku_matrix)):
        for column in range(len(sudoku_matrix)):
            if sudoku_matrix[row][column] == 0:
                row_solutions = row_possible_solutions_besides_selected_cell(sudoku_matrix, row, column)     
                if len(row_solutions) == 1:
                    sudoku_matrix[row][column] = row_solutions[0]
    return sudoku_matrix


# This function returns list of possible solutions in each cell in the column besides the cell selected. This will be used in the next function
def column_possible_solutions_besides_selected_cell(sudoku_matrix, row, column):
    unique_solutions = cell_possible_solutions(sudoku_matrix, row, column)
    solutions = []
    for x in range(len(sudoku_matrix)):
        if sudoku_matrix[x][column] == 0 and x != row:
            solutions += cell_possible_solutions(sudoku_matrix, x, column)
    for number in solutions:
        if number in unique_solutions:
            unique_solutions.remove(number)
    return unique_solutions

# This function checks for possible solution for the current cell, if one of those numbers is present only in that specific cell out of the whole column, it places it into the cell and updates the sudoku matrix (then returns it after going through it once)    
def cell_has_solution_that_no_other_cell_has_in_column(sudoku_matrix):
    for row in range(len(sudoku_matrix)):
        for column in range(len(sudoku_matrix)):
            if sudoku_matrix[row][column] == 0:
                column_solutions = column_possible_solutions_besides_selected_cell(sudoku_matrix, row, column)     
                if len(column_solutions) == 1:
                    sudoku_matrix[row][column] = column_solutions[0]
    return sudoku_matrix


# This function returns list of possible solutions in each cell in the column besides the cell selected. This will be used in the next function
def square_possible_solutions_besides_selected_cell(sudoku_matrix, row, column):
    coordinates = square_cells(correct_square_finder(row, column))
    unique_solutions = cell_possible_solutions(sudoku_matrix, row, column)
    solutions = []
    for x in range(0, 3):
        for y in range(0, 3):
            if sudoku_matrix[coordinates[x]][coordinates[y+3]] == 0 and not (coordinates[x] == row and coordinates[y+3] == column):
                solutions = solutions + cell_possible_solutions(sudoku_matrix, coordinates[x], coordinates[y+3])
    for number in solutions:
        if number in unique_solutions:
            unique_solutions.remove(number)
    return unique_solutions



# This function checks for possible solution for the current cell, if one of those numbers is present only in that specific cell out of the whole square, it places it into the cell and updates the sudoku matrix (then returns it after going through it once)
def cell_has_solution_that_no_other_cell_has_in_square(sudoku_matrix):
    for row in range(len(sudoku_matrix)):
        for column in range(len(sudoku_matrix)):
            if sudoku_matrix[row][column] == 0:
                square_solutions = square_possible_solutions_besides_selected_cell(sudoku_matrix, row, column)     
                if len(square_solutions) == 1:
                    sudoku_matrix[row][column] = square_solutions[0]
    return sudoku_matrix


# This function calculates sum of all row cells
def sum_row_cells(sudoku_matrix, row):
    sum = 0
    for number in row_contents(row, sudoku_matrix):
        sum += number
    return sum


# This function calculates sum of all column cells
def sum_column_cells(sudoku_matrix, column):
    sum = 0
    for number in column_contents(column, sudoku_matrix):
        sum += number
    return sum


# This function calculates sum of all square cells
def sum_square_cells(sudoku_matrix, row, column):
    sum = 0
    for number in square_contents(correct_square_finder(row, column), sudoku_matrix):
        sum += number
    return sum


# This function checks if the sudoku is solved (correctly) by checking if every row, column and square has value that add up to 45, which has to be true by definition.
def solution_correctness_check(sudoku_solved):
    #for x in sudoku_solved:
    #    print(x)
    for row in range(len(sudoku_solved)):
        for column in range(len(sudoku_solved)):
            if (sum_row_cells(sudoku_solved, row) == 45) and (sum_column_cells(sudoku_solved, column) == 45) and (sum_square_cells(sudoku_solved, row, column) == 45):
                continue
            else:
                return False
    return True

# This function congregates all 4 of the solving functions and calls them over and over until the sudoku is fully solved. upon solving, it returns the solved sudoku matrix
def perform_magic(sudoku_matrix):
    while not solution_correctness_check(sudoku_matrix):
        sudoku_matrix = cell_has_one_possible_solution(sudoku_matrix)  
        sudoku_matrix = cell_has_solution_that_no_other_cell_has_in_row(sudoku_matrix)
        sudoku_matrix = cell_has_solution_that_no_other_cell_has_in_column(sudoku_matrix)
        sudoku_matrix = cell_has_solution_that_no_other_cell_has_in_square(sudoku_matrix)
    return sudoku_matrix


def main():
    # Change later for user input
    sudoku_matrix_inputed = [[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]
    
    # This function creates and displays the grid for the sudoku to be inserted in
    def create_grid(root, sudoku_matrix):
        entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry_var = tk.StringVar()  # StringVar to store the entry value
                value = sudoku_matrix[i][j]
                if value == 0:
                    entry = tk.Entry(root, width=2, font=('Arial', 14), textvariable=entry_var)
                else:
                    entry = tk.Label(root, width=2, font=('Arial', 14), textvariable=entry_var)
                entry_var.set('' if value == 0 else str(value))  # Display empty cells instead of zeros
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry_var)
            entries.append(row)
        return entries
    
    # This function updates the contents in the gui/showing the whole sudoku after it is solved by the program
    def update_grid(entries, sudoku_matrix):
        for i in range(9):
            for j in range(9):
                entry_var = entries[i][j]
                value = sudoku_matrix[i][j]
                entry_var.set('' if value == 0 else str(value))  # Display empty cells instead of zeros

    # This function saves all the data the user entered into the sudoku_matrix
    def input_button_click(entries, sudoku_matrix):
        for i in range(9):
            for j in range(9):
                entry_var = entries[i][j]
                value = entry_var.get()
                sudoku_matrix[i][j] = int(value) if value.isdigit() else 0  # Convert to int if valid number, otherwise set to 0
        update_grid(entries, sudoku_matrix)

    root = tk.Tk()
    root.title("Sudoku Solver")

    # Example sudoku matrix
    sudoku_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def solve(result_matrix):
        sudoku_matrix = result_matrix

    grid_entries = create_grid(root, sudoku_matrix)

    input_button = tk.Button(root, text="Solve", command=lambda: [input_button_click(grid_entries, sudoku_matrix), solve(perform_magic(sudoku_matrix)), update_grid(grid_entries, sudoku_matrix)])
    input_button.grid(row=10, columnspan=9, padx=1, pady=10)

    root.mainloop()

# Call main and wait for magic to solve your sudoku
main()