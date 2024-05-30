import tkinter as tk
from tkinter import messagebox
import random
from copy import deepcopy

# direction matrix
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
# target matrix
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Puzzle solving code
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)
    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))
    return listNode

def getBestNode(openSet):
    firstIter = True
    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = []
    while node.dir:
        dir_map = {"U": "move up", "D": "move down", "L": "move left", "R": "move right"}
        branch.append({'dir': dir_map[node.dir], 'node': node.current_node})
        node = closedSet[str(node.previous_node)]
    branch.append({'dir': '', 'node': node.current_node})
    branch.reverse()
    return branch


def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    closed_set = {}
    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node
        if test_node.current_node == END:
            return buildPath(closed_set)
        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node
        del open_set[str(test_node.current_node)]

# GUI code
class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.initUI()

    def initUI(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, font=('Helvetica', 20), width=4, height=2,
                                   command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.shuffle)
        self.shuffle_button.pack(side="left", padx=20, pady=20)
        
        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.pack(side="right", padx=20, pady=20)

        self.puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.update_buttons()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                num = self.puzzle[i][j]
                if num == 0:
                    self.buttons[i][j].config(text="", bg="lightgray")
                else:
                    self.buttons[i][j].config(text=str(num), bg="white")

    def move_tile(self, i, j):
        empty_i, empty_j = get_pos(self.puzzle, 0)
        if (abs(empty_i - i) == 1 and empty_j == j) or (abs(empty_j - j) == 1 and empty_i == i):
            self.puzzle[empty_i][empty_j], self.puzzle[i][j] = self.puzzle[i][j], self.puzzle[empty_i][empty_j]
            self.update_buttons()
            if self.puzzle == END:
                messagebox.showinfo("8-Puzzle Game", "You solved the puzzle!")

    def shuffle(self):
        def get_valid_moves(state):
            empty_pos = get_pos(state, 0)
            moves = []
            for direction, (di, dj) in DIRECTIONS.items():
                ni, nj = empty_pos[0] + di, empty_pos[1] + dj
                if 0 <= ni < 3 and 0 <= nj < 3:
                    new_state = deepcopy(state)
                    new_state[empty_pos[0]][empty_pos[1]] = new_state[ni][nj]
                    new_state[ni][nj] = 0
                    moves.append(new_state)
            return moves

        # Start with the solved state
        self.puzzle = deepcopy(END)

        # Perform a large number of random moves to shuffle
        num_shuffles = 999
        for _ in range(num_shuffles):
            moves = get_valid_moves(self.puzzle)
            self.puzzle = random.choice(moves)

        self.update_buttons()

    def solve(self):
        path = main(self.puzzle)
        for step in path[1:]:
            self.puzzle = step['node']
            self.update_buttons()
            self.root.update()
            self.root.after(500)
        self.show_solution(path)

    def show_solution(self, path):
        steps = [step['dir'] for step in path if step['dir']]
        message = "Solution steps:\n" + "\n".join(steps)
        messagebox.showinfo("8-Puzzle Solution", message)

if __name__ == '__main__':
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()