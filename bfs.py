import numpy as np
from collections import deque

class Puzzle: #パズルの状態を管理する
    def __init__(self, board):
        # ボードの状態を初期化
        self.board = np.array(board)
        # 0(空白のタイル)の位置を取得
        location = np.where(self.board == 0)
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
        visited = set([self.start.board.tobytes()]) # 一度訪れた状態を記録 set():順番を持たず、重複されるものは取り除かれるリスト tobytes():Byte型に変換
        parent_map = {self.start.board.tobytes(): None} # {パズルの状態を表すバイト列: 親のPuzzleオブジェクト}
        total_states_explored = 0

        while queue:
            current_puzzle = queue.popleft() # popleft():queueの先頭から要素を一つ削除し、その値を返す
            total_states_explored += 1

            if np.array_equal(current_puzzle.board, self.goal.board): # ゴールの状態と一致しているかを比較する。
                return self.get_path(parent_map, current_puzzle), total_states_explored, len(visited)

            for neighbor in current_puzzle.get_possible_moves():
                if neighbor.board.tobytes() not in visited:
                    queue.append(neighbor) # queueの末尾にneighborを追加
                    visited.add(neighbor.board.tobytes())
                    parent_map[neighbor.board.tobytes()] = current_puzzle

        return None, total_states_explored, len(visited)

    def get_path(self, parent_map, goal):
        path = []
        current = goal

        while current is not None:
            path.append(current.board.tolist()) # NumPy配列をリストに変換
            current = parent_map[current.board.tobytes()]

        return path[::-1] # 配列を逆順にして返す

start_board = [
    [1, 2, 3],
    [5, 0, 6],
    [4, 7, 8]
]

goal_board = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# パズルの開始状態とゴール状態を設定
graph = PuzzleGraph(start_board, goal_board)

# 幅優先探索で解を探す
solution_path, total_states_explored, total_unique_states = graph.bfs()

# 解が存在すれば表示
if solution_path is not None:
    print(f'解答までの総ステップ数: {len(solution_path) - 1}')
    print(f'探索した総状態数: {total_states_explored}')
    # print(f'探索したユニークな状態数: {total_unique_states}')

    for step, board in enumerate(solution_path):
        print(f'\nステップ {step}')
        print(np.array(board))
else:
    print('解答が見つかりませんでした。')