############################################################
# CMPSC 442: Homework 2
############################################################
import math

student_name = "Sishi Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
from collections import Counter
from collections import deque
import random


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    f = math.factorial
    return int(f(n * n) / (f(n) * f(n * n - n)))


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    c = Counter()
    for queen in board:
        c[queen] = c[queen] + 1
    for value in c.values():
        if value > 1:
            return False
    if len(board) == 2:
        if board == [0, 1] or board == [1, 0]:
            return False
    for (r1, c) in enumerate(board):
        for r2 in range(r1 + 1, len(board)):
            if abs(r1 - r2) == abs(c - board[r2]):
                return False
    return True


def n_queens_helper(n, board):
    return [board + [i] for i in range(0, n, 1)]


def n_queens_solutions(n):
    frontier = n_queens_helper(n, [])
    while frontier:
        board = frontier.pop()
        if n_queens_valid(board):
            if len(board) == n:
                yield board
            else:
                frontier.extend(n_queens_helper(n, board))


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.row = len(board)
        self.column = len(board[0])
        self.dimension = (self.row, self.column)

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if row > 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if row < self.row - 1:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if col > 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        if col < self.column - 1:
            self.board[row][col + 1] = not self.board[row][col + 1]

    def scramble(self):
        for row in range(self.row):
            for col in range(self.column):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for x in range(self.row):
            for y in range(self.column):
                if self.board[x][y]:
                    return False
        return True

    def copy(self):
        new = []
        for x in self.board:
            temp = x[:]
            new.append(temp)
        return LightsOutPuzzle(new)

    def successors(self):
        for x in range(self.row):
            for y in range(self.column):
                move = (x, y)
                new = self.copy()
                new.perform_move(x, y)
                yield move, new

    def find_solution(self):
        initial = tuple(tuple(self.get_board()[i]) for i in range(len(self.get_board())))
        if self.is_solved():
            return []
        frontier = deque([self])
        pre_dic = {}
        while frontier:
            state = frontier.popleft()
            for (next_move, next_state) in state.successors():
                temp = tuple(tuple(next_state.get_board()[i]) for i in range(len(next_state.get_board())))
                if next_state.is_solved():
                    move_path = deque()
                    move_path.append(next_move)
                    next_state.perform_move(next_move[0], next_move[1])
                    temp = tuple(tuple(next_state.get_board()[i]) for i in range(len(next_state.get_board())))
                    while temp != initial:
                        next_move = pre_dic[temp]
                        move_path.appendleft(next_move)
                        next_state.perform_move(next_move[0], next_move[1])
                        temp = tuple(tuple(next_state.get_board()[i]) for i in range(len(next_state.get_board())))
                    return list(move_path)
                if pre_dic.get(temp) is None:
                    pre_dic[temp] = next_move
                    frontier.append(next_state)
        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for j in range(cols)] for i in range(rows)])


############################################################
# Section 3: Linear Disk Movement
############################################################
class IdenticalDisk(object):

    def __init__(self, s, l):
        self.disk_set = s
        self.length = l
        self.n = len(s)

    def get_set(self):
        return self.disk_set

    def perform_move(self, f, t):
        if abs(t - f) == 1 and t not in self.disk_set:
            self.disk_set.discard(f)
            self.disk_set.add(t)
        if abs(t - f) == 2 and t not in self.disk_set:
            if f < t and (f + 1) in self.disk_set:
                self.disk_set.discard(f)
                self.disk_set.add(t)
            if f > t and (f - 1) in self.disk_set:
                self.disk_set.discard(f)
                self.disk_set.add(t)

    def is_solved(self):
        for x in range(self.length - self.n):
            if x in self.disk_set:
                return False
        return True

    def copy(self):
        new = set()
        for x in self.disk_set:
            new.add(x)
        return IdenticalDisk(new, self.length)

    def successors(self):
        for val in self.disk_set:
            if (val + 1) < self.length:
                move = (val, val + 1)
                new = self.copy()
                new.perform_move(val, val + 1)
                yield move, new

            if (val - 1) >= 0:
                move = (val, val - 1)
                new = self.copy()
                new.perform_move(val, val - 1)
                yield move, new

            if (val + 2) < self.length:
                move = (val, val + 2)
                new = self.copy()
                new.perform_move(val, val + 2)
                yield move, new

            if (val - 2) >= 0:
                move = (val, val - 2)
                new = self.copy()
                new.perform_move(val, val - 2)
                yield move, new

    def find_solution(self):
        initial = tuple(self.get_set())
        if self.is_solved():
            return []
        frontier = deque([self])
        pre_dic = {}
        while frontier:
            state = frontier.popleft()
            for (next_move, next_state) in state.successors():
                temp = tuple(next_state.get_set())
                if next_state.is_solved():
                    move_path = deque()
                    move_path.append(next_move)
                    next_state.perform_move(next_move[1], next_move[0])
                    temp = tuple(next_state.get_set())
                    while temp != initial:
                        next_move = pre_dic[temp]
                        move_path.appendleft(next_move)
                        next_state.perform_move(next_move[1], next_move[0])
                        temp = tuple(next_state.get_set())
                    return list(move_path)
                if pre_dic.get(temp) is None:
                    pre_dic[temp] = next_move
                    frontier.append(next_state)
        return None


def create_idential(length, n):
    disk_set = set()
    for i in range(n):
        disk_set.add(i)
    return IdenticalDisk(disk_set, length)


def solve_identical_disks(length, n):
    p = create_idential(length, n)
    return p.find_solution()


class DistinctDisk(object):

    def __init__(self, dic, l, n):
        self.disk_dic = dic
        self.length = l
        self.n = n

    def get_dic(self):
        return self.disk_dic

    def perform_move(self, f, t):
        if abs(t - f) == 1 and self.disk_dic[t] == -1:
            self.disk_dic[t] = self.disk_dic[f]
            self.disk_dic[f] = -1
        if abs(t - f) == 2 and self.disk_dic[t] == -1:
            if f < t and self.disk_dic[f + 1] != -1:
                self.disk_dic[t] = self.disk_dic[f]
                self.disk_dic[f] = -1
            if f > t and self.disk_dic[f - 1] != -1:
                self.disk_dic[t] = self.disk_dic[f]
                self.disk_dic[f] = -1

    def is_solved(self):
        temp = self.n - 1
        for x in range(self.length - self.n, self.length):
            if self.disk_dic[x] != temp:
                return False
            temp -= 1
        return True

    def copy(self):
        new = {}
        for key, value in self.disk_dic.items():
            new[key] = value
        return DistinctDisk(new, self.length, self.n)

    def successors(self):
        for key in self.disk_dic:
            if (key + 1) < self.length:
                move = (key, key + 1)
                new = self.copy()
                new.perform_move(key, key + 1)
                yield move, new

            if (key - 1) >= 0:
                move = (key, key - 1)
                new = self.copy()
                new.perform_move(key, key - 1)
                yield move, new

            if (key + 2) < self.length:
                move = (key, key + 2)
                new = self.copy()
                new.perform_move(key, key + 2)
                yield move, new

            if (key - 2) >= 0:
                move = (key, key - 2)
                new = self.copy()
                new.perform_move(key, key - 2)
                yield move, new

    def find_solution(self):
        initial = tuple((i, self.get_dic()[i]) for i in range(self.length))
        if self.is_solved():
            return []
        frontier = deque([self])
        pre_dic = {}
        while frontier:
            state = frontier.popleft()
            for (next_move, next_state) in state.successors():
                temp = tuple((i, next_state.get_dic()[i]) for i in range(next_state.length))
                if next_state.is_solved():
                    move_path = deque()
                    move_path.append(next_move)
                    next_state.perform_move(next_move[1], next_move[0])
                    temp = tuple((i, next_state.get_dic()[i]) for i in range(next_state.length))
                    while temp != initial:
                        next_move = pre_dic[temp]
                        move_path.appendleft(next_move)
                        next_state.perform_move(next_move[1], next_move[0])
                        temp = tuple((i, next_state.get_dic()[i]) for i in range(next_state.length))
                    return list(move_path)
                if pre_dic.get(temp) is None:
                    pre_dic[temp] = next_move
                    frontier.append(next_state)
        return None


def create_distinct(length, n):
    disk_dic = {}
    disk = 0
    for i in range(length):
        if disk < n:
            disk_dic[i] = disk
        else:
            disk_dic[i] = -1
        disk += 1
    return DistinctDisk(disk_dic, length, n)


def solve_distinct_disks(length, n):
    p = create_distinct(length, n)
    return p.find_solution()


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
I spent approximately 22 hours on this assignment .
"""

feedback_question_2 = """
I found out that last question is the most challenging. 
Because I did not got the correct answers.
"""

feedback_question_3 = """
To be honest, I like the whole assignment.
It's good exercise for me. In my opinion, nothing need to be changed.
"""
