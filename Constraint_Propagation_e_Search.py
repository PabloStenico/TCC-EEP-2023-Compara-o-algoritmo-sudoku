import time
import os

def cross(A, B):
    return [a + b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in squares)

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def search(values):
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def some(seq):
    for e in seq:
        if e:
            return e
    return False

def solve(grid):
    start_time = time.time()
    solution = search(parse_grid(grid))
    end_time = time.time()
    time_taken = end_time - start_time
    return solution, time_taken

def read_sudoku_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    return ["".join(data[i:i+9]) for i in range(0, len(data), 9)]

def write_sudoku_to_file(file_path, sudoku_number, solved_sudoku, time_taken):
    with open(file_path, 'a') as file:
        file.write(f'Sudoku {sudoku_number} resolvido em {time_taken} segundos:\n')
        for key, value in sorted(solved_sudoku.items()):
            file.write(value + " ")
            if int(key[1]) % 9 == 0:
                file.write("\n")
        file.write("\n")

if __name__ == '__main__':
    input_file_path = 'diabolico.txt'
    output_file_path = 'sudoku_output.txt'
    total_time = 0

    if not os.path.isfile(input_file_path):
        print(f'O arquivo {input_file_path} não existe.')
        exit(1)

    sudoku_puzzles = read_sudoku_from_file(input_file_path)

    for i, puzzle in enumerate(sudoku_puzzles, start=1):
        solved_sudoku, time_taken = solve(puzzle)
        total_time += time_taken
        if solved_sudoku:
            write_sudoku_to_file(output_file_path, i, solved_sudoku, time_taken)
        else:
            print("Nenhuma solução encontrada.")
    
    with open(output_file_path, 'a') as file:
        file.write(f'Tempo total para resolver todos os Sudokus: {total_time} segundos\n')
