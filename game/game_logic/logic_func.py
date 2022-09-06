def is_in_chess_board(pos: str) -> bool:
    return ord('A') <= ord(pos[0]) <= ord('H') and 1 <= int(pos[1]) <= 8


def change_pos_name(pos: str, x: int, y: int) -> str:
    letter_changed = 'Z' if ord(pos[0])+x < ord('A') else chr(ord(pos[0])+x)
    return letter_changed + str(int(pos[1])+y)
