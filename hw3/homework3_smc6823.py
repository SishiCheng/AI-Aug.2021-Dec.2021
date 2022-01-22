############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Sishi Cheng"

############################################################
# Imports
############################################################
import random
import math
from collections import deque
from queue import PriorityQueue


# Include your imports here, if any are used.


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    tile_num = 1
    board = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            board[i][j] = tile_num
            tile_num += 1
    board[i][j] = 0
    return TilePuzzle(board)


def trace_back_move(direction):
    if direction == "up":
        return "down"
    elif direction == "down":
        return "up"
    elif direction == "left":
        return "right"
    elif direction == "right":
        return "left"


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.row = len(board)
        self.column = len(board[0])
        self.dimension = (self.row, self.column)
        for i in range(self.row):
            for j in range(self.column):
                if board[i][j] == 0:
                    self.empty_row = i
                    self.empty_col = j

        self.move = 0

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        flag = False
        if (direction != "up") and (direction != "down") and (direction != "left") and (direction != "right"):
            return False
        if (direction == "up") and (self.empty_row - 1 >= 0):
            self.board[self.empty_row][self.empty_col] = self.board[self.empty_row - 1][self.empty_col]
            self.board[self.empty_row - 1][self.empty_col] = 0
            self.empty_row = self.empty_row - 1
            return True
        if (direction == "down") and (self.empty_row + 1 < self.row):
            self.board[self.empty_row][self.empty_col] = self.board[self.empty_row + 1][self.empty_col]
            self.board[self.empty_row + 1][self.empty_col] = 0
            self.empty_row = self.empty_row + 1
            return True
        if (direction == "left") and (self.empty_col - 1 >= 0):
            self.board[self.empty_row][self.empty_col] = self.board[self.empty_row][self.empty_col - 1]
            self.board[self.empty_row][self.empty_col - 1] = 0
            self.empty_col = self.empty_col - 1
            return True
        if (direction == "right") and (self.empty_col + 1 < self.column):
            self.board[self.empty_row][self.empty_col] = self.board[self.empty_row][self.empty_col + 1]
            self.board[self.empty_row][self.empty_col + 1] = 0
            self.empty_col = self.empty_col + 1
            return True
        return False

    def scramble(self, num_moves):
        directions = ["up", "down", "left", "right"]
        for i in range(num_moves):
            self.perform_move(random.choice(directions))

    def is_solved(self):
        solved = create_tile_puzzle(self.row, self.column)
        if self.board == solved.get_board():
            return True
        return False

    def copy(self):
        new = []
        for x in self.board:
            temp = x[:]
            new.append(temp)
        return TilePuzzle(new)

    def successors(self):
        new_up = self.copy()
        if new_up.perform_move("up"):
            yield "up", new_up
        new_down = self.copy()
        if new_down.perform_move("down"):
            yield "down", new_down
        new_left = self.copy()
        if new_left.perform_move("left"):
            yield "left", new_left
        new_right = self.copy()
        if new_right.perform_move("right"):
            yield "right", new_right

    def iddfs_helper(self, limit, move):
        if self.board == create_tile_puzzle(self.row, self.column).get_board():
            yield move
        elif limit > len(move):
            for new_move, new_p in self.successors():
                for solution in new_p.iddfs_helper(limit, move + [new_move]):
                    yield solution

    # Required
    def find_solutions_iddfs(self):
        if self.is_solved():
            return []
        flag = False
        limit = 0
        while not flag:
            for path in self.iddfs_helper(limit, []):
                yield path
                flag = True
            limit += 1

    def h_n(self):
        return abs(self.empty_row + 1 - self.row) + abs(self.empty_col + 1 - self.column)

    def __lt__(self, other):
        return self.get_board() < other.get_board()

    # Required
    def find_solution_a_star(self):
        frontier = PriorityQueue()
        frontier.put((0 + self.h_n(), self))
        initial = tuple(tuple(self.get_board()[i]) for i in range(len(self.get_board())))
        visited = []
        if self.is_solved():
            return []
        pre_dic = {}
        while not frontier.empty():
            state = frontier.get()[1]
            visited.append(state.get_board())
            state_temp = tuple(tuple(state.get_board()[i]) for i in range(len(state.get_board())))
            if state.is_solved():
                move_path = deque()
                move_path.append(pre_dic[state_temp])
                state.perform_move(trace_back_move(pre_dic[state_temp]))
                temp = tuple(tuple(state.get_board()[i]) for i in range(len(state.get_board())))
                while temp != initial:
                    next_dir = pre_dic[temp]
                    move_path.appendleft(next_dir)
                    state.perform_move(trace_back_move(next_dir))
                    temp = tuple(tuple(state.get_board()[i]) for i in range(len(state.get_board())))
                return list(move_path)

            for (next_dir, next_state) in state.successors():
                if next_state.get_board() in visited:
                    continue
                next_state.move = state.move + 1
                frontier.put((next_state.move + next_state.h_n(), next_state))
                #temp_next = tuple(tuple(next_state.get_board()[i]) for i in range(len(next_state.get_board())))
                #cost = move_cost[state_temp] + 1

                #if temp_next not in move_cost or move_cost[temp_next] > cost:
                    #move_cost[temp_next] = cost
                    #frontier.put((cost + next_state.h_n(), next_state))
                temp = tuple(tuple(next_state.get_board()[i]) for i in range(len(next_state.get_board())))
                if pre_dic.get(temp) is None:
                        pre_dic[temp] = next_dir
        return None


b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
p = TilePuzzle(b)
print(list(p.find_solution_a_star()))


############################################################
# Section 2: Grid Navigation
############################################################

class Grid(object):
    def __init__(self, start, goal, scene):
        self.start = start
        self.goal = goal
        self.scene = scene
        self.row = len(self.scene)
        self.column = len(self.scene[0])

    def euclidean(self, start, goal):
        return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

    def perform_move(self, position, direction):
        if (direction == "up") and (position[0] - 1 >= 0):
            if self.scene[position[0] - 1][position[1]]:
                return False
            return True
        if (direction == "down") and (position[0] + 1 < self.row):
            if self.scene[position[0] + 1][position[1]]:
                return False
            return True
        if (direction == "left") and (position[1] - 1 >= 0):
            if self.scene[position[0]][position[1] - 1]:
                return False
            return True
        if (direction == "right") and (position[1] + 1 < self.column):
            if self.scene[position[0]][position[1] + 1]:
                return False
            return True
        if (direction == "up-left") and (position[0] - 1 >= 0) and (position[1] - 1 >= 0):
            if self.scene[position[0] - 1][position[1] - 1]:
                return False
            return True
        if (direction == "up-right") and (position[0] - 1 >= 0) and (position[1] + 1 < self.column):
            if self.scene[position[0] - 1][position[1] + 1]:
                return False
            return True
        if (direction == "down-left") and (position[0] + 1 < self.row) and (position[1] - 1 >= 0):
            if self.scene[position[0] + 1][position[1] - 1]:
                return False
            return True
        if (direction == "down-right") and (position[0] + 1 < self.row) and (position[1] + 1 < self.column):
            if self.scene[position[0] + 1][position[1] + 1]:
                return False
            return True
        return False

    def grid_successors(self, position):
        if self.perform_move(position, "up"):
            yield position[0] - 1, position[1]
        if self.perform_move(position, "down"):
            yield position[0] + 1, position[1]
        if self.perform_move(position, "left"):
            yield position[0], position[1] - 1
        if self.perform_move(position, "right"):
            yield position[0], position[1] + 1
        if self.perform_move(position, "up-left"):
            yield position[0] - 1, position[1] - 1
        if self.perform_move(position, "up-right"):
            yield position[0] - 1, position[1] + 1
        if self.perform_move(position, "down-left"):
            yield position[0] + 1, position[1] - 1
        if self.perform_move(position, "down-right"):
            yield position[0] + 1, position[1] + 1

    def find_solution(self):
        frontier = PriorityQueue()
        frontier.put((0, self.start))
        move_cost = {self.start: 0}
        visited = []
        if self.scene[self.start[0]][self.start[1]] or self.scene[self.goal[0]][self.goal[1]]:
            return None
        if self.start == self.goal:
            return []
        pre_dic = {}
        # is_found = False
        # move = 0
        while not frontier.empty():
            state = frontier.get()[1]
            # print('frontier')
            # print(state)
            visited.append(state)
            # print('visited')
            # print(state)
            # print(visited)
            if state == self.goal:
                # is_found = True
                move_path = deque()
                move_path.append(state)
                while state != self.start:
                    # move_path.append(state)
                    state = pre_dic[state]
                    # next_dir = pre_dic[state]
                    # move_path.appendleft(next_dir)
                    move_path.appendleft(state)
                    # state = next_dir
                return list(move_path)

            for next_state in self.grid_successors(state):
                # print(next_state)
                if next_state in visited:
                    # print('enter')
                    continue
                cost = move_cost[state] + self.euclidean(state, next_state)
                # print(cost)

                if next_state not in move_cost or move_cost[next_state] > cost:
                    move_cost[next_state] = cost
                    # pre_dic[next_state] = state
                    frontier.put((cost + self.euclidean(next_state, self.goal), next_state))
                    pre_dic[next_state] = state
            # print('frontier')
            # print(cost + euclidean(next_state, goal))
        return None


def find_path(start, goal, scene):
    grid = Grid(start, goal, scene)

    return grid.find_solution()


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
class DistinctDisk(object):

    def __init__(self, dic, l, n):
        self.disk_dic = dic
        self.length = l
        self.n = n
        self.move = 0

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

    def h_n(self):
        move = 0
        for i in range(self.length):
            if self.disk_dic[i] != -1:
                move += abs(self.length - 1 - i - self.disk_dic[i])
        return move

    def __lt__(self, other):
        return self.move < other.move

    def find_solution(self):
        frontier = PriorityQueue()
        frontier.put((0 + self.h_n(), self))
        visited = []
        initial = tuple((i, self.get_dic()[i]) for i in range(self.length))
        if self.is_solved():
            return []
        pre_dic = {}
        while not frontier.empty():
            state = frontier.get()[1]
            visited.append(state.get_dic())
            state_temp = tuple((i, state.get_dic()[i]) for i in range(state.length))
            if state.is_solved():
                move_path = deque()
                move_path.append(pre_dic[state_temp])
                state.perform_move(pre_dic[state_temp][1], pre_dic[state_temp][0])
                temp = tuple((i, state.get_dic()[i]) for i in range(state.length))
                while temp != initial:
                    next_move = pre_dic[temp]
                    move_path.appendleft(next_move)
                    state.perform_move(next_move[1], next_move[0])
                    temp = tuple((i, state.get_dic()[i]) for i in range(state.length))
                return list(move_path)

            for (next_dir, next_state) in state.successors():
                if next_state.get_dic() in visited:
                    continue
                next_state.move = state.move + 1
                frontier.put((next_state.move + next_state.h_n(), next_state))
                temp = tuple((i, next_state.get_dic()[i]) for i in range(next_state.length))
                if pre_dic.get(temp) is None:
                    pre_dic[temp] = next_dir
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


# print(solve_distinct_disks(5, 3))


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for j in range(cols)] for i in range(rows)])


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.row = len(board)
        self.column = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        for i in range(self.row):
            for j in range(self.column):
                self.board[i][j] = False

    def is_legal_move(self, row, col, vertical):
        if 0 <= row < self.row and 0 <= col < self.column:
            if self.board[row][col]:
                return False
            if vertical:
                if row + 1 < self.row and not self.board[row + 1][col]:
                    return True
                else:
                    return False
            else:
                if col + 1 < self.column and not self.board[row][col + 1]:
                    return True
                else:
                    return False
        return False

    def legal_moves(self, vertical):
        for i in range(self.row):
            for j in range(self.column):
                if self.is_legal_move(i, j, vertical):
                    yield i, j

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            if vertical:
                self.board[row + 1][col] = True
            else:
                self.board[row][col + 1] = True

    def game_over(self, vertical):
        if list(self.legal_moves(vertical)):
            return False
        return True

    def copy(self):
        new = []
        for x in self.board:
            temp = x[:]
            new.append(temp)
        return DominoesGame(new)

    def successors(self, vertical):
        for x in range(self.row):
            for y in range(self.column):
                move = (x, y)
                new = self.copy()
                if self.is_legal_move(x, y, vertical):
                    new.perform_move(x, y, vertical)
                    yield move, new

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(-float('inf'), float('inf'), vertical, limit, None)

    def max_value(self, alpha, beta, vertical, limit, curr_m):

        if self.game_over(vertical) or limit == 0:
            return curr_m, len(list(self.successors(vertical))) - len(list(self.successors(not vertical))), 1
        v = -float('inf')

        visit = 0
        # temp_m = curr_m
        for loc, child in self.successors(vertical):
            move, value, visited = child.min_value(alpha, beta, not vertical, limit - 1, loc)
            visit += visited
            if value > v:
                v = value
                curr_m = loc
            if v >= beta:
                return curr_m, v, visit
            alpha = max(alpha, v)
        return curr_m, v, visit

    def min_value(self, alpha, beta, vertical, limit, curr_m):
        if self.game_over(vertical) or limit == 0:
            return curr_m, len(list(self.successors(not vertical))) - len(list(self.successors(vertical))), 1
        v = float('inf')

        visit = 0
        # temp_m = curr_m
        for loc, child in self.successors(vertical):
            move, value, visited = child.max_value(alpha, beta, not vertical, limit - 1, loc)
            visit += visited
            if value < v:
                v = value
                curr_m = loc
            if v <= alpha:
                return curr_m, v, visit
            beta = min(beta, v)
        return curr_m, v, visit


# g = create_dominoes_game(4, 4)
# g2 = g.copy()
# g.perform_move(0, 0, True)
# print(g.get_board() == g2.get_board())
# print(g.get_board())
# g.perform_move(1, 0, False)
# print(g.get_board())
# b = [[False] * 3 for i in range(3)]
# g = DominoesGame(b)
# g.perform_move(0, 1, True)
# print(g.get_best_move(False, 1))
# print(g.get_best_move(True, 1))
# print(list(g.legal_moves(True)))
# print(g.is_legal_move(0, 0, True))
# print(g.is_legal_move(0, 0, False))
############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
I spent approximately 24 hours on this assignment .
"""

feedback_question_2 = """
I found out that first question is the most challenging. 
Because I did not set up a good visited queue, the program went in to the loop.
I spent about three hours to fix that, it help me have a better understanding of A* search algorithm.
"""

feedback_question_3 = """
To be honest, I like the whole assignment.
It's good exercise for me. In my opinion, nothing need to be changed.
"""
