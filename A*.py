import numpy as np
from collections import deque
import heapq

class Puzzle:
    def __init__(self, board, g=0, h=0):
        self.board = np.array(board)
        location = np.where(self.board == 0)
        self.empty_tile_location = (location[0][0], location[1][0])
        self.g = g  # コスト(開始状態から現在の状態までのコスト)
        self.h = h  # ヒューリスティック値(現在の状態から目標の状態までのコスト)
        self.f = self.g + self.h  # 合計コスト

    def get_possible_moves(self):
        row, col = self.empty_tile_location
        possible_moves = []

        # 空白のタイルを上に動かす
        if row > 0:
            new_board = self.board.copy()
            new_board[row, col], new_board[row-1, col] = new_board[row-1, col], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist()))

        # 空白のタイルを下に動かす
        if row < 2:
            new_board = self.board.copy()
            new_board[row, col], new_board[row+1, col] = new_board[row+1, col], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist()))

        # 空白のタイルを左に動かす
        if col > 0:
            new_board = self.board.copy()
            new_board[row, col], new_board[row, col-1] = new_board[row, col-1], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist()))

        # 空白のタイルを右に動かす
        if col < 2:
            new_board = self.board.copy()
            new_board[row, col], new_board[row, col+1] = new_board[row, col+1], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist()))

        return possible_moves

    def calculate_heuristic(self, goal):
        return sum(abs(b % 3 - g % 3) + abs(b//3 - g//3)
                   for b, g in ((self.board[i,j], goal[i,j])
                                for i in range(3) for j in range(3)))

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        return hash(str(self.board))

    def __lt__(self, other):
        return self.f < other.f


def a_star(start, goal):
    heap = [(start.f, start)]
    visited = set([start])

    while heap:
        current = heapq.heappop(heap)[1]
        if current == goal:
            return current.g, len(visited)  # 総ステップ数と総状態数を返す
        for child in current.get_possible_moves():
            if child not in visited or child.g < current.g:
                child.g = current.g + 1
                child.h = child.calculate_heuristic(goal.board)
                child.f = child.g + child.h
                heapq.heappush(heap, (child.f, child))
                visited.add(child)
    return False


# 入力データの例
start_board = [
    [1, 2, 3],
    [5, 0, 6],
    [4, 7, 8]
]

goal_board = [
    [1, 2, 3],
    [5, 8, 6],
    [0, 7, 4]
]

start = Puzzle(start_board)
goal = Puzzle(goal_board)

steps, states = a_star(start, goal)  # 総ステップ数と総状態数を取得
print(f"総ステップ数: {steps}, 総状態数: {states}")
