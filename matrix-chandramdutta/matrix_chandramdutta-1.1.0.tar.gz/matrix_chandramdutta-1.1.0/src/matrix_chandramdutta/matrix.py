def get_matrix_input(rows: int, columns: int) -> list:
    matrix = []
    for row in range(rows):
        matrix.append([])
        for column in range(columns):
            matrix[row].append(
                input(f"Enter element at row {row + 1} and column {column + 1}: "))
    return matrix


def get_matrix_zero(rows: int, columns: int) -> list:
    matrix = []
    for row in range(rows):
        matrix.append([])
        for column in range(columns):
            matrix[row].append(0)
    return matrix


def add_two_matrix(matrix_one: list, matrix_two: list) -> list:
    result = []
    for row in range(len(matrix_one)):
        result.append([])
        for column in range(len(matrix_one[0])):
            result[row].append(matrix_one[row][column] +
                               matrix_two[row][column])
    return result


def subtract_two_matrix(matrix_one: list, matrix_two: list) -> list:
    result = []
    for row in range(len(matrix_one)):
        result.append([])
        for column in range(len(matrix_one[0])):
            result[row].append(matrix_one[row][column] -
                               matrix_two[row][column])
    return result


def multiply_two_matrix(matrix_one: list, matrix_two: list) -> list:
    result = []
    for row in range(len(matrix_one)):
        result.append([])
        for column in range(len(matrix_two[0])):
            result[row].append(0)
            for k in range(len(matrix_two)):
                result[row][column] += matrix_one[row][k] * \
                    matrix_two[k][column]
    return result


def print_matirx(matrix: list):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            print(matrix[row][column], end=" ")
        print()
