import random

main_board = {7: " ", 8: " ", 9: " ", 4: " ", 5: " ", 6: " ", 1: " ", 2: " ", 3: " "}
state = {"X": "Player 1", "O": "Player 2"}
game_over = False

##At depth = -1; Random. depth = 1; Intermediate. At depth = 2; Impossible
depth = 2


# prints the board
def print_board(board=main_board):
    x = 0
    y = 0
    for element in board:
        print(f" {board[element]} ", end="")
        if x == 0 or x == 1:
            print("|", end="")
        x += 1
        if x > 2 and y < 2:
            x = 0
            y += 1
            print("\n" + "-" * 11)


# inserts at a given position the state required
def insert_at(position, state, board=main_board):
    board[position] = state
    return board


# decides turn of either X or O
def decide_turn(board=main_board):
    x, o = 0, 0
    for element in board:
        if board[element] == "X":
            x += 1
        if board[element] == "O":
            o += 1

    if x == o:
        return "X"
    return "O"


# checks if board has space and returns True or False
def has_board_space(board=main_board):
    if " " in board.values():
        return True
    return False


# checks the state of the game and returns winner X or O or " " (means no winner)
def game_state(board=main_board, not_test=True):
    global game_over
    board_list = list(board.values())

    def check_vertical():
        for x in range(3):
            if board_list[x] == " ":
                continue
            if (
                board_list[x] == board_list[x + 3]
                and board_list[x + 3] == board_list[x + 6]
            ):
                return board_list[x]

    def check_horizontal():
        for x in range(0, 9, 3):
            if board_list[x] == " ":
                continue
            if (
                board_list[x] == board_list[x + 1]
                and board_list[x + 1] == board_list[x + 2]
                and board_list[x] != " "
            ):
                return board_list[x]

    def check_diagonal():
        for x in [0, 2]:
            if board_list[x] == " ":
                continue
            try:
                if (
                    board_list[x] == board_list[x + 4]
                    and board_list[x + 4] == board_list[x + 8]
                    and board_list[x] != " "
                ):
                    return board_list[x]
            except:
                if (
                    board_list[x] == board_list[x + 2]
                    and board_list[x + 2] == board_list[x + 4]
                ):
                    return board_list[x]

    winner = " "
    if check_vertical() != None:
        winner = check_vertical()
    elif check_horizontal() != None:
        winner = check_horizontal()
    elif check_diagonal() != None:
        winner = check_diagonal()

    if not_test and (winner != " " or not has_board_space(board)):
        game_over = True

    return winner


# establishes a player vs player
def player_vs_player():
    global main_board, game_over
    board = main_board
    while not game_over:
        print()
        print_board(board)
        print()

        # takes in position
        position = int(
            input(
                f"\n{state[decide_turn(board)]} enter the position of {decide_turn(board)}(1-9): "
            )
        )

        while position < 1 or position > 9 or board[position] != " ":
            print("Invalid!")
            position = int(
                input(
                    f"\n{state[decide_turn(board)]} enter the position of {decide_turn(board)}(1-9): "
                )
            )

        board = insert_at(position, decide_turn(board))
        winner = game_state(board)

    print_board(board)
    if winner != " ":
        print(f"\nThe winner is {state[winner]}.")
    else:
        print("\nThe game was a draw.")


def evaluate(board=main_board):
    # Check rows, columns, and diagonals for a winner
    if decide_turn() == "X":
        opponent_mark = "O"
    else:
        opponent_mark = "X"

    for i in range(1, 4):
        row = [board[i] for i in range((i - 1) * 3 + 1, i * 3 + 1)]
        if len(set(row)) == 1 and row[0] != " ":
            return 1 if row[0] == opponent_mark else -1

    for i in range(1, 4):
        col = [board[j] for j in range(i, i + 7, 3)]
        if len(set(col)) == 1 and col[0] != " ":
            return 1 if col[0] == opponent_mark else -1

    if len(set(board[i] for i in range(1, 10, 4))) == 1 and board[1] != " ":
        return 1 if board[1] == opponent_mark else -1

    if len(set(board[i] for i in range(3, 8, 2))) == 1 and board[3] != " ":
        return 1 if board[3] == opponent_mark else -1

    return 0  # No winner, the game is a draw


# returns the optimal position of play
def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    if score != 0:
        return score

    if " " not in board.values():
        return 0  # The board is full, and it's a draw

    min_mark = decide_turn()
    if min_mark == "X":
        max_mark = "O"
    else:
        max_mark = "X"

    if is_maximizing:
        max_eval = float("-inf")
        for i in range(1, 10):
            if board[i] == " ":
                board[i] = max_mark
                eval = minimax(board, depth + 1, False)
                board[i] = " "
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(1, 10):
            if board[i] == " ":
                board[i] = min_mark
                eval = minimax(board, depth + 1, True)
                board[i] = " "
                min_eval = min(min_eval, eval)
        return min_eval


# machine returns the position it wants to play
def machine_return(board=main_board, depth=depth):
    board_list = list(board.values())
    if board_list.count(" ") == 9 or depth == -1:
        move = random.randint(1, 9)
        while board[move] != " ":
            move = random.randint(1, 9)
        return move

    best_val = float("-inf")
    best_move = None

    machine_mark = decide_turn()
    if machine_mark == "X":
        opponent_mark = "O"
    else:
        opponent_mark = "X"

    for i in range(1, 10):
        if board[i] == " ":
            board[i] = opponent_mark
            move_val = minimax(board, 0, False)
            board[i] = " "

            if move_val > best_val:
                best_move = i
                best_val = move_val

    if depth != 0:
        board_copy = board.copy()
        board_copy = insert_at(best_move, machine_mark, board_copy)
        opponent_move = machine_return(board_copy, depth - 1)
        board_copy = insert_at(opponent_move, opponent_mark, board_copy)
        if game_state(board_copy, False) == opponent_mark:
            return opponent_move

    return best_move


# establishes a player vs machine
def player_vs_machine():
    global state, main_board
    board = main_board
    player_mark = input("Enter the mark you want to play [X/O]: ").upper()
    if player_mark == "X":
        state["O"] = "Machine"
    else:
        state["X"] = "Machine"

    while not game_over:
        print()
        print_board(board)
        print()

        if state[decide_turn(board)] == "Machine":
            position = machine_return(board)
            board = insert_at(position, decide_turn(board))
            winner = game_state(board)
            print()
            continue

        # takes in position from player
        position = int(
            input(
                f"\n{state[decide_turn(board)]} enter the position of {decide_turn(board)}(1-9): "
            )
        )

        while position < 1 or position > 9 or board[position] != " ":
            print("Invalid!")
            position = int(
                input(
                    f"\n{state[decide_turn(board)]} enter the position of {decide_turn(board)}(1-9): "
                )
            )

        board = insert_at(position, decide_turn(board))
        winner = game_state(board)

    print_board(board)
    try:
        if winner != " ":
            print(f"\nThe winner is {state[winner]}.")
        else:
            print("\nThe game was a draw.")
    except UnboundLocalError:
        pass


# returns none, simple terminal user interface
def main():
    global depth
    play = True
    while play:
        print("\n\n\n**************Tic Tac Toe**************\n")
        print("1.Player vs Player")
        print("2.Player vs Machine")
        print("0.Exit")

        choice = int(input("\nEnter your choice[0,1,2]: "))
        if choice == 0:
            play = False
        elif choice == 1:
            player_vs_player()
        elif choice == 2:
            print("0.Easy\n1.Medium\n2.Hard")
            level = int(input("Level[0,1,2]: "))
            while not (level <= 2 and level >= 0):
                print("Invalid level!")
                level = int(input("Level[0,1,2]: "))

            if level == 0:
                depth = -1
            else:
                depth = level

            player_vs_machine()
        else:
            play = False
            print("You have entered an option out of scope.\nExiting.\n")


main()
