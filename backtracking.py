import time
import numpy as np

def is_valid(board, row, col, num):
    # Verifica se o número já está na linha
    if num in board[row]:
        return False

    # Verifica se o número já está na coluna
    for r in range(9):
        if board[r][col] == num:
            return False

    # Verifica se o número já está no quadrante 3x3
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True


def solve_sudoku(board):
    # Encontra a próxima célula vazia
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # Sudoku resolvido

    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True  # Continua a solução com o número atual

            board[row][col] = 0  # Backtrack, desfaz a decisão e tenta outro número

    return False  # Nenhuma solução encontrada


def find_empty_cell(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))


def read_sudoku_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    sudokus = []
    sudoku = []
    for i, line in enumerate(lines):
        row = list(map(int, line.strip()))
        sudoku.append(row)

        # Se já temos 9 linhas ou chegamos ao final do arquivo, adicionamos o sudoku à lista
        if (i+1) % 9 == 0:
            sudokus.append(sudoku)
            sudoku = []

    return sudokus


def write_solution_to_file(filename, solutions):
    with open(filename, 'w') as f:
        for solution, duration in solutions:
            f.write(f"Solução encontrada em {duration} segundos:\n")
            for row in solution:
                f.write(" ".join(str(num) for num in row))
                f.write("\n")
            f.write("\n")


def main():
    sudokus = read_sudoku_from_file('especialista.txt')
    total_time = 0
    with open('sudoku_solutions.txt', 'w') as f:
        for i, sudoku in enumerate(sudokus, 1):
            start_time = time.time()
            if solve_sudoku(sudoku):
                end_time = time.time()
                duration = end_time - start_time
                total_time += duration
                f.write(f'Sudoku {i} resolvido em {duration} segundos:\n')
                for row in sudoku:
                    f.write(' '.join(str(num) for num in row) + '\n')
                f.write('\n')
            else:
                f.write(f'Sudoku {i} não tem solução.\n\n')
        f.write(f'Tempo total para resolver todos os Sudokus: {total_time} segundos\n')

if __name__ == "__main__":
    main()
