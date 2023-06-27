import numpy as np
from collections import deque

class Puzzle:
    def __init__(self, board):
        self.board = np.array(board)
        location = np.where(self.board == 0)
        self.empty_tile_location = (location[0][0], location[1][0])

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

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        return hash(str(self.board))


def dfs(start, goal):
    stack = deque([start])
    visited = set([start])
    steps = 0  # 追加：ステップ数をカウントする変数

    while stack:
        node = stack.pop()
        steps += 1  # 追加：探索を開始するたびにステップ数を増やす
        if node == goal:
            return True, steps, len(visited)  # 追加：結果、ステップ数、探索した状態数を返す
        for child in node.get_possible_moves():
            if child not in visited:
                visited.add(child)
                stack.append(child)
    return False, steps, len(visited)  # 追加：結果、ステップ数、探索した状態数を返す


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

result, steps, states = dfs(start, goal)  # 結果、ステップ数、探索した状態数を受け取る

print(f"総ステップ: {steps}, 総状態数: {states}")
