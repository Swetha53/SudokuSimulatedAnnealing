import copy
import numpy as np
import random
import time
import math

max_iteration = 400000
def print_sudoku(Sudoku):
    print("|------|------|------|")
    for i in range(9):
        print("|", end="")
        for j in range(9):
            print(Sudoku[(9*i)+j], end=" ")
            if j % 3 == 2:
                print("|", end="")
        print()
        if i % 3 == 2:
            print("|------|------|------|")

def get_block_indices(k, ignore_originals = False):
    rowOffset = (k // 3) * 3
    colOffset = (k % 3) * 3
    indices = [colOffset + (j % 3) + 9*(rowOffset + (j // 3)) for j in range(9)]
    if ignore_originals:
        indices = filter(lambda x:x not in NonFixedEntries, indices)
    return indices

def get_row_indices(row):
    indices = [j + 9 * row for j in range(9)]
    return indices

def get_col_indices(col):
    indices = [col + 9 * j for j in range(9)]
    return indices

def randomized_solution():
    for i in range(9):
        blockIndices = get_block_indices(i)
        block = Sudoku[blockIndices]
        zeroIndices = [idx for i, idx in enumerate(blockIndices) if block[i] == 0]
        activeOptions = [i for i in range(1, 10) if i not in block]
        random.shuffle(activeOptions)
        for idx, value in zip(zeroIndices, activeOptions):
            Sudoku[idx] = value

def sudoku_score(Sudoku):
    score = 0
    for i in range(9):
        setRow = set(Sudoku[get_row_indices(i)])
        setCol = set(Sudoku[get_col_indices(i)])
        score += len(setRow) + len(setCol)
    return score

def refine_solution(Sudoku):
    newSolution = copy.deepcopy(Sudoku)
    block = random.randint(0, 8)
    total = len(list(get_block_indices(block, True)))
    randomCells = random.sample(range(total), 2)
    cell1, cell2 = [list(get_block_indices(block, True))[idx] for idx in randomCells]
    newSolution[cell1], newSolution[cell2] = newSolution[cell2], newSolution[cell1]
    return newSolution
def sudoku_solver(Sudoku):
    print("Original Puzzle:")
    print_sudoku(Sudoku)
    randomized_solution()
    bestSudoku = copy.deepcopy(Sudoku)
    currentScore = sudoku_score(Sudoku)
    bestScore = currentScore
    T = .5
    iteration = 0

    while iteration < max_iteration:
        try:
            if iteration % 1000 == 0:
                print("Iteration %s, \tT = %.5f, \tBest Score = %s, \tCurrent Score = %s" % (iteration, T, bestScore, currentScore))
            refinedSolution = refine_solution(Sudoku)
            refinedSolutionScore = sudoku_score(refinedSolution)

            # parameter delta
            delta = float(refinedSolutionScore - currentScore)

            if math.exp(delta / T) - random.random() > 0:
                Sudoku = refinedSolution
                currentScore = refinedSolutionScore

            if currentScore > bestScore:
                bestSudoku = copy.deepcopy(Sudoku)
                bestScore = currentScore

            if refinedSolutionScore == 162:
                Sudoku = refinedSolution
                break

            # Change in Temperature
            T = .9999 * T
            iteration += 1
        except:
            print("Hit an unknown error.")

    print("Iteration %s, \tT = %.5f, \tBest Score = %s, \tCurrent Score = %s" % (iteration, T, bestScore, currentScore))
    if bestScore == 162:
        print("\n Solved the Puzzle!!")
    else:
        print("\n Didn't solve the Puzzle. (%s/%s points)"%(bestScore, 162))
    print("\n Final Puzzle:")
    print_sudoku(bestSudoku)

if __name__ == "__main__":
    startTime = time.time()
    file = open("sudoku_inputs/evil03.txt", "r")
    Sudoku = []
    row = []
    for line in file:
        if line.strip():
            Sudoku = Sudoku + [int(i) for i in line.strip()]
    BlankPuzzle = np.array(Sudoku)
    Sudoku = copy.deepcopy(BlankPuzzle)
    NonFixedEntries = np.arange(81)[Sudoku > 0]
    sudoku_solver(Sudoku)
    print("Execution Time: ", time.time() - startTime)
