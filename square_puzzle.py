
from random import randint

edge_length = 3
squares = [] #Squareクラスを収納
space = [edge_length - 1, edge_length - 1] #パネルのない場所の位置(row, col)
count = 0 #目的の配置になるまで何回パネルを動かしたかどうかのカウント
answersquares = [] #答えの状態を保存
puzzle_states = [] #すべてのパズルの状態を保持。

class SquarePuzzle:
    def __init__(self, board, count):
        self.board = board #状態の管理
        self.count = count #初期状態から何回動かした状態かをカウントする。

class Square:
    def __init__(self, name, col, row):
        self.name = name
        self.col = col
        self.row = row

def set_board():
    global squares, answersquares
    for i in range(edge_length ** 2):
        col = i % edge_length
        row = i // edge_length

        squares.append(Square(i + 1, col, row))
    squares[edge_length ** 2 - 1].name = 0
    answersquares = squares

def set_randam(shuffle_count):
    global space
    for _ in range(shuffle_count):
        actions = []
        if space[0] - 1 >= 0:
            actions.append([-1,0]) #左
        if space[0] + 1 < edge_length:
            actions.append([1,0]) #右
        if space[1] - 1 >= 0:
            actions.append([0,-1]) #上
        if space[1] + 1 < edge_length:
            actions.append([0,1]) #下
        action = actions[randint(0, len(actions) - 1)]
        space_number = space[1] * edge_length + space[0] #現在パネルがない場所の配列の位置
        change_square = squares[space_number + (action[1] * edge_length + action[0])] #次に空白になるパネルの位置
        squares[space_number].name = change_square.name
        space = [change_square.col, change_square.row]
        change_square.name = 0

def show_squares():
    for square in squares:
        print(square.name, square.col, square.row)

def show_board():
    board = []
    for square in squares:
        board.append(square.name)
    print('')
    show_text = ''
    for row in range(edge_length):
        for col in range(edge_length):
            show_text += str(board[row * edge_length + col])
        print(show_text)
        show_text = ''

# def move_panel(current_state, before_state):
#     global puzzle_states
#     actions = []
#     if space[0] - 1 >= 0:
#         actions.append([-1,0]) #左
#     if space[0] + 1 < edge_length:
#         actions.append([1,0]) #右
#     if space[1] - 1 >= 0:
#         actions.append([0,-1]) #上
#     if space[1] + 1 < edge_length:
#         actions.append([0,1]) #下
#     for action in actions:
#         space_number = space[1] * edge_length + space[0] #現在パネルがない場所の配列の位置
#         change_square = squares[space_number + (action[1] * edge_length + action[0])] #次に空白になるパネルの位置
#         squares[space_number].name = change_square.name
#         space = [change_square.col, change_square.row]
#         change_square.name = 0
#         changed_state = SquarePuzzle(, current_state.count+1)
#         if ( !== current_state.board):
#         puzzle_states.append()

def play_bfs():
    global puzzle_states
    puzzle_states.append(SquarePuzzle(squares, 0))




def play():
    set_board()
    show_board()
    set_randam(1000)
    show_board()


play()

