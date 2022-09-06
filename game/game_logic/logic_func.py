def is_in_chess_board(pos: str) -> bool:
    return ord('A') <= ord(pos[0]) <= ord('H') and 1 <= int(pos[1]) <= 8


def change_pos_name(pos: str, x: int, y: int) -> str:
    letter_changed = 'Z' if ord(pos[0])+x < ord('A') else chr(ord(pos[0])+x)
    return letter_changed + str(int(pos[1])+y)


def get_moves_as_long_as_they_are_legal(start_pos: str, board: dict[str], x_ch: int, y_ch: int) -> list[str]:
    act_pos = change_pos_name(start_pos, x_ch, y_ch)
    while is_in_chess_board(act_pos):
        if board[act_pos] != '':
            yield act_pos
            break
        yield act_pos
        act_pos = change_pos_name(act_pos, x_ch, y_ch)


def get_all_moves_in_given_directions(start_pos: str, board: dict[str], dirs: list[tuple[int, int]]) -> list[str]:
    moves = []
    for dir_ in dirs:
        moves.extend(get_moves_as_long_as_they_are_legal(start_pos, board, dir_[0], dir_[1]))
    return moves
