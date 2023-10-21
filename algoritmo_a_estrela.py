import heapq
import numpy as np
import time
import os

class SudokuNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.priority = 0
        self.heuristic = 0

    def __lt__(self, other):
        return self.priority < other.priority

def is_goal(state):
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                return False
    return True

def get_possible_values(state, row, col):
    values = set(range(1, 10))
    values -= set(state[row, :])
    values -= set(state[:, col])

    box_row, box_col = row // 3 * 3, col // 3 * 3
    values -= set(state[box_row:box_row + 3, box_col:box_col + 3].flatten())

    return values

def get_next_unassigned(state):
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                return i, j
    return None

def a_star(sudoku_board):
    start_time = time.time()
    root = SudokuNode(sudoku_board)
    root.heuristic = get_heuristic(sudoku_board)
    root.priority = root.heuristic

    open_set = []
    heapq.heappush(open_set, root)

    while open_set:
        current = heapq.heappop(open_set)
        if is_goal(current.state):
            return current.state, time.time() - start_time

        row, col = get_next_unassigned(current.state)
        if row is None or col is None:
            continue

        possible_values = get_possible_values(current.state, row, col)
        for value in possible_values:
            next_state = current.state.copy()
            next_state[row][col] = value
            next_node = SudokuNode(next_state, parent=current, action=(row, col, value))
            next_node.heuristic = get_heuristic(next_state)
            next_node.priority = next_node.heuristic
            heapq.heappush(open_set, next_node)

    return None

def get_heuristic(state):
    return 81 - np.count_nonzero(state)

def read_sudoku_from_file(file_path):
    sudoku_puzzles = []
    with open(file_path, 'r') as file:
        data = file.readlines()
        for i in range(0, len(data), 9):
            sudoku_board = np.array([list(map(int, list(line.strip()))) for line in data[i:i+9]])
            sudoku_puzzles.append(sudoku_board)
    return sudoku_puzzles

def write_sudoku_to_file(file_path, sudoku_number, solved_sudoku, time_taken):
    with open(file_path, 'a') as file:
        file.write(f'Sudoku {sudoku_number} resolvido em {time_taken} segundos:\n')
        for row in solved_sudoku:
            file.write(' '.join(map(str, row)) + '\n')
        file.write('\n')

if __name__ == "__main__":
    input_file_path = 'diabolico.txt'
    output_file_path = 'sudoku_output.txt'
    total_time = 0

    if not os.path.isfile(input_file_path):
        print(f'O arquivo {input_file_path} não existe.')
        exit(1)

    sudoku_puzzles = read_sudoku_from_file(input_file_path)

    for i, puzzle in enumerate(sudoku_puzzles, start=1):
        solution, time_taken = a_star(puzzle)
        total_time += time_taken
        if solution is not None:
            write_sudoku_to_file(output_file_path, i, solution, time_taken)
        else:
            print("Não foi possível encontrar uma solução.")
    
    with open(output_file_path, 'a') as file:
        file.write(f'Tempo total para resolver todos os Sudokus: {total_time} segundos\n')
