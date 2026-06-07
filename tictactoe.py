import random


win_patterns = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],

        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],

        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]


def create_board():
    board_space = []
    for start in range(1, 10, 3):
        board_space.append([str(start), str(start + 1), str(start + 2)])
    return board_space


def display_board(board):
    print()
    for row in board:
        print('|'.join(row))
        print('-' * 5)
    print()


def make_move(board, spot, move="O", name="Computer"):
    try:
        spot = int(spot)
        if spot > 9 or spot < -1:
            print("\nOops! Wrong spot there. Please choose from 1-9!\n")
            return False
        row = (spot - 1) // 3
        col = (spot - 1) % 3
        if board[row][col] in ["X", "O"]:
            print(f"Position {spot} already taken. Please choose another spot.")
            return False
        else:
            board[row][col] = move
            print(f"{name} successfully made a move at position {spot}!")
            display_board(board)
            return True
    except ValueError:
        return False


# Defensive AI function
def check_def_spot(board):
    # Check the pattern and return the defensive spot coordinates.
    # If the pattern contains two X and an empty spot, return the coordinates.
    for pattern in win_patterns:
        x_count = 0
        o_count = 0
        empty_spot = -1
        for r, c in pattern:
            curr_spot = board[r][c]
            if curr_spot == 'X':
                x_count += 1
            elif curr_spot == 'O':
                o_count += 1
            else:
                empty_spot = board[r][c]
            
        if empty_spot not in ['X', 'O'] and (x_count == 2 and o_count == 0):
            return empty_spot
            
    return -1


# Offensive AI function
def make_offensive_move(board, spot = -1):
    # This function should try to build moves based on the winning patterns.
    # Check any previous move and add another move.
    if spot != -1:
        return make_move(board, spot)
    for pattern in win_patterns:
        o_count = 0
        x_count = 0
        empty_spot = 0
        for r, c in pattern:
            curr_spot = board[r][c]
            if curr_spot == 'O':
                o_count += 1
            elif curr_spot == 'X':
                x_count += 1
            else:
                empty_spot = curr_spot
        if empty_spot not in ['X', 'O'] and (o_count == 1 and x_count == 0):
            return make_move(board, empty_spot)
    return make_move(board, random.randint(1, 9))


def check_winner(board, player = "O"):
    for pattern in win_patterns:
        won = True  # assume this pattern is a win

        for r, c in pattern:
            # check each position in the pattern
            if board[r][c] != player:
                # if any cell is not the player's symbol,
                # this pattern is not a win
                won = False
                break  # stop checking this pattern early

        if won:
            # if no mismatches were found, player wins
            return True


def is_draw(board):
    for row in board:
        for cell in row:
            if cell not in ["X", "O"]:
                return False
    return True


def check_input(user_input):
    try:
        if user_input is None:
            return False
        user_input = int(user_input)
        return True
    except ValueError:
        return False


def whose_turn():
    is_turn = input("\nWho do want to pick first?\nPress 1: Player\nPress 2: Computer\nType here: ")
        
    if is_turn == "1":
        print("Your turn first!\n")
        return True
    elif is_turn == "2":
        print("The computer will pick first!\n")
        return False
    else:
        print("\nYou've entered an invalid answer. The computer will pick first!\n")
        return False


def play_game():
    player_name = input("Who are you? Type your name: ").capitalize()
    current_board = create_board()
    input_error = False
    loop_count = 0
    is_turn = "computer" if not whose_turn() else "player"

    while True:
        # Computer Turn
        if is_turn == "computer":
            print("Computer is making a move...\n")
            def_spot = check_def_spot(current_board)
            if def_spot != -1:
                if not make_offensive_move(current_board, def_spot):
                    continue
                is_turn = "player"
            else:
                if not make_offensive_move(current_board):
                    continue
                is_turn = "player"

            if check_winner(current_board):
                print("Computer wins! Try again.\n")
                break

            if is_draw(current_board):
                print("Oops! It seems like you both won!\n")
                break

        # Player Turn
        if is_turn == "player":
            if not input_error:
                print(f"Hello, {player_name}! Please make a move..." if loop_count == 0 else f"It's your turn now, {player_name}! Make a move.")
                prompt = "Enter a number between 1-9 as your position. Or type -1 to exit: "
            else:
                prompt = "Oops! Try again: "
            
            player_input = input(prompt)

            if not check_input(player_input):
                print("Please enter a valid number!")
                input_error = True
                continue

            if player_input == '-1':
                print("You've exited the game!")
                break
            
            if not make_move(current_board, player_input, 'X', player_name):
                input_error = True
            else:
                input_error = False
                is_turn = "computer"

            if check_winner(current_board, 'X'):
                print(f"\nCongratrulations, {player_name}! You've beat the odds!")
                break

            if is_draw(current_board):
                print("Woah! It's a draw!")
                break
        
        loop_count += 1
        

play_game()