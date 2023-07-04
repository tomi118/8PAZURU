import numpy as np
import heapq

class Puzzle:
    def __init__(self, board, g=0, h=0):
        # ボードの状態を初期化
        self.board = np.array(board)
        # 0(空白のタイル)の位置を取得
        location = np.where(self.board == 0)
        self.empty_tile_location = (location[0][0], location[1][0])
        self.g = g  # コスト(開始状態から現在の状態までのコスト)
        self.h = h  # ヒューリスティック値(現在の状態から目標の状態までのコスト)
        self.f = self.g + self.h  # 合計コスト

    def get_possible_moves(self):
        # 空白のタイルが動ける全ての方向を取得
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

    def calculate_heuristic(self, goal): # 現在の状態からゴールまでの推定コストを計算する。
        # abs:絶対値を返す。 b:現在のパズルの位置, g:目標のパズルの位置
        return sum(abs(b % 3 - g % 3) + abs(b//3 - g//3) #最大値は4
                   for b, g in ((self.board[i,j], goal[i,j])
                                for i in range(3) for j in range(3)))

    def __lt__(self, other): # heapq モジュールを使ったプライオリティキューで使用される。ヒューリスティック値が小さいパズルオブジェクトを優先的にキューから取り出すために使用される。
        return self.f < other.f

class PuzzleGraph:
    def __init__(self, start, goal):
        self.start = Puzzle(start)
        self.goal = Puzzle(goal)

    def a_star(self):
        heap = [(self.start.f, self.start)]
        visited = set([self.start.board.tobytes()])
        parent_map = {self.start.board.tobytes(): None} # {パズルの状態を表すバイト列: 親のPuzzleオブジェクト}
        total_states_explored = 0

        while heap:
            current = heapq.heappop(heap)[1] #heapq.heappop(heap):ヒープから最小の要素（つまり最小の合計コストを持つ状態）を削除し、それを返す。
            total_states_explored += 1

            if np.array_equal(current.board, self.goal.board):
                return self.get_path(parent_map, current), total_states_explored

            for move in current.get_possible_moves():
                move.h = move.calculate_heuristic(self.goal.board)
                move.f = move.g + move.h
                if move.board.tobytes() not in visited:
                    heapq.heappush(heap, (move.f, move))
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
path, states_explored = graph.a_star()

# 探索の結果の出力
print(f'解答までの総ステップ数: {len(path) - 1}')
print(f"探索した総状態数: {states_explored}")

for i, board in enumerate(path):
    print(f'\nステップ {i}')
    print(np.array(board))

