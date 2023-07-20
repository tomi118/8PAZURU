#初期状態を生成するためのプログラム

import random
import numpy as np

#ボードが解けるかどうかを判定する。
def is_solvable(board): #board:ボードを表現する1次元リスト
    inv_count = 0
    for i in range(8): #[0,1,2,3,4,5,6,7,8]
        for j in range(i + 1, 9):
            # iがjより前に出現し、かつi > jとなるペア(i, j)の数をカウントする
            if (board[j] and board[i] and board[i] > board[j]):
                inv_count += 1

    # 転倒数が偶数であればボードは解けると判断する
    return (inv_count % 2 == 0) #ボードが解けるならTrue、そうでないならFalse


#8パズルゲームの初期ボードを作成する。
def create_initial_board():

    while True:
        board = list(range(1, 9)) + [0]  # 0は空きスペースを表す
        random.shuffle(board)

        # ボードが解けるものであれば、2次元配列に変換して返す
        if is_solvable(board):
            return np.array(board).reshape((3, 3)).tolist() #初期ボードを表現する2次元配列


# 使用例
initial_board = create_initial_board()
print(initial_board)
