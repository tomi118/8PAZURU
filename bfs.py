import numpy as np
from collections import deque

class Puzzle: #パズルの状態を管理する
    def __init__(self, board):
        self.board = np.array(board) # ボードの状態を初期化
        location = np.where(self.board == 0) # 0(空白のタイル)の位置を取得
        self.empty_tile_location = (location[0][0], location[1][0])

    def get_possible_moves(self):
        # 空白のタイルが動ける全ての方向を取得
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

class PuzzleGraph: # 探索木全体を管理
    def __init__(self, start, goal):
        self.start = Puzzle(start)
        self.goal = Puzzle(goal)

    def bfs(self):
        queue = deque([self.start])
        parent_map = {self.start.board.tobytes(): None} # {パズルの状態を表すバイト列: 親のPuzzleオブジェクト}
        visited = set([self.start.board.tobytes()]) # 一度訪れた状態を記録 set():順番を持たず、重複されるものは取り除かれるリスト tobytes():Byte型に変換
        total_states_explored = 0

        while queue:
            current = queue.popleft() # popleft():queueの先頭から要素を一つ削除し、その値を返す
            total_states_explored += 1

            if np.array_equal(current.board, self.goal.board): # ゴールの状態と一致しているかを比較する。
                return self.get_path(parent_map, current), total_states_explored, len(visited)

            for neighbor in current.get_possible_moves():
                if neighbor.board.tobytes() not in visited:
                    queue.append(neighbor) # queueの末尾にneighborを追加
                    visited.add(neighbor.board.tobytes())
                    parent_map[neighbor.board.tobytes()] = current

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

# パズルの開始状態とゴール状態を設定
graph = PuzzleGraph(start_board, goal_board)

# 幅優先探索で解を探す
path, total_states_explored, total_unique_states = graph.bfs()

# 探索の結果の出力
print(f'解答までの総ステップ数: {len(path) - 1}')
print(f'探索した総状態数: {total_states_explored}')
print(f'探索したユニークな状態数: {total_unique_states}')

for i, board in enumerate(path):
    print(f'\nステップ {i}')
    print(np.array(board))
