import numpy as np
from collections import deque
import heapq

class Puzzle:
    def __init__(self, board, g=0, h=0):
        self.board = np.array(board) # ボードの状態を初期化
        location = np.where(self.board == 0) # 0(空白のタイル)の位置を取得
        self.empty_tile_location = (location[0][0], location[1][0])
        self.g = g  # 開始状態から現在の状態まで何回動かしたか
        self.h = h  # ヒューリスティック値(現在の状態から目標の状態までのコスト)

    def get_possible_moves(self):
        row, col = self.empty_tile_location
        possible_moves = []

        # 空白のタイルを上に動かす
        if row > 0:
            new_board = self.board.copy()
            new_board[row, col], new_board[row-1, col] = new_board[row-1, col], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist(), self.g+1))

        # 空白のタイルを下に動かす
        if row < 2:
            new_board = self.board.copy()
            new_board[row, col], new_board[row+1, col] = new_board[row+1, col], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist(), self.g+1))

        # 空白のタイルを左に動かす
        if col > 0:
            new_board = self.board.copy()
            new_board[row, col], new_board[row, col-1] = new_board[row, col-1], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist(), self.g+1))

        # 空白のタイルを右に動かす
        if col < 2:
            new_board = self.board.copy()
            new_board[row, col], new_board[row, col+1] = new_board[row, col+1], new_board[row, col]
            possible_moves.append(Puzzle(new_board.tolist(), self.g+1))

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
        return self.h < other.h


class PuzzleGraph: # 探索木全体を管理
    def __init__(self, start, goal):
        self.start = Puzzle(start)
        self.goal = Puzzle(goal)

    def heuristic(self):
        heap = [(self.start.h, self.start)]
        parent_map = {self.start.board.tobytes(): None} # {パズルの状態を表すバイト列: 親のPuzzleオブジェクト}
        visited = set([self.start.board.tobytes()]) # 一度訪れた状態を記録 set():順番を持たず、重複されるものは取り除かれるリスト tobytes():Byte型に変換
        total_states_explored = 0

        while heap:
            current = heapq.heappop(heap)[1] #heapq.heappop(heap):ヒープから最小の要素（つまり最小の合計コストを持つ状態）を削除し、それを返す。
            total_states_explored += 1

            if np.array_equal(current.board, self.goal.board):
                return self.get_path(parent_map, current), total_states_explored

            for move in current.get_possible_moves():
                move.h = move.calculate_heuristic(self.goal.board)
                if move.board.tobytes() not in visited:
                    heapq.heappush(heap, (move.h, move))
                    visited.add(move.board.tobytes())
                    parent_map[move.board.tobytes()] = current

        return None

    def get_path(self, parent_map, goal):
        path = []
        current = goal

        while current is not None:
            path.append(current.board.tolist()) # NumPy配列をリストに変換
            current = parent_map[current.board.tobytes()]

        return path[::-1] # 配列を逆順にして返す


# スタートとゴールの状態
start_board =[[0, 8, 3],[5, 2, 4],[6, 7, 1]]
goal_board = [[1,2,3],[4,5,6],[7,8,0]]

# 探索の実行
graph = PuzzleGraph(start_board, goal_board)
path, states_explored = graph.heuristic()

# 探索の結果の出力
print(f'解答までの総ステップ数: {len(path) - 1}')
print(f"探索した総状態数: {states_explored}")
for i, board in enumerate(path):
    print(f"Step {i}")
    print(np.array(board))
