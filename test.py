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

class PuzzleGraph:
    def __init__(self, start, goal):
        # 開始状態とゴール状態を設定
        self.start = Puzzle(start)
        self.goal = Puzzle(goal)

    def bfs(self):
        # BFS(幅探索)を使用して解を探す
        queue = deque([self.start])
        visited = set([self.start.board.tobytes()])
        parent_map = {self.start.board.tobytes(): None}

        while queue:
            current_puzzle = queue.popleft()

            # ゴール状態に達したかをチェック
            if np.array_equal(current_puzzle.board, self.goal.board):
                return self.get_path(parent_map, current_puzzle)

            # 可能な全ての次の状態に対して
            for neighbor in current_puzzle.get_possible_moves():
                # まだ訪れていない状態だけを調査
                if neighbor.board.tobytes() not in visited:
                    visited.add(neighbor.board.tobytes())
                    parent_map[neighbor.board.tobytes()] = current_puzzle
                    queue.append(neighbor)

        # 解がない場合はNoneを返す
        return None

    def get_path(self, parent_map, goal):
        path = []
        current = goal

        while current is not None:
            path.append(current.board.tolist())
            current = parent_map[current.board.tobytes()]

        return path[::-1]

start_board = [[8, 5, 7],
               [3, 1, 6],
               [2, 4, 0]]

goal_board = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# パズルの開始状態とゴール状態を設定
graph = PuzzleGraph(start_board, goal_board)

# 幅優先探索で解を探す
solution_path = graph.bfs()

# 解が存在すれば表示
if solution_path is not None:
    for step, board in enumerate(solution_path):
        print(f'Step {step}')
        print(np.array(board), '\n')
else:
    print('No solution found.')