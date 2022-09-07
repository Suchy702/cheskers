def is_in_chess_board(pos: str) -> bool:
    return ord('A') <= ord(pos[0]) <= ord('H') and 1 <= int(pos[1]) <= 8


def is_in_checker_board(pos: str) -> bool:
    return pos[0] in "ZABCDEFGHI" and 0 <= int(pos[1]) <= 9


def is_checker_on_pos(obj: str) -> bool:
    return obj == 'C'


def is_chess_on_pos(obj: str) -> bool:
    return obj != 'C' and obj != ''


def change_pos_name(pos: str, x: int, y: int) -> str:
    letter_changed = 'Z' if ord(pos[0]) + x < ord('A') else chr(ord(pos[0]) + x)
    return letter_changed + str(int(pos[1]) + y)


def get_starting_board() -> dict[str, str]:
    board = {
        "Z9": "", "A9": "", "B9": "C", "C9": "", "D9": "C", "E9": "", "F9": "C", "G9": "", "H9": "C", "I9": "",
        "Z8": "", "A8": "C", "B8": "", "C8": "C", "D8": "", "E8": "C", "F8": "", "G8": "C", "H8": "", "I8": "",
        "Z7": "", "A7": "", "B7": "C", "C7": "", "D7": "C", "E7": "", "F7": "C", "G7": "", "H7": "C", "I7": "",
        "Z6": "", "A6": "", "B6": "", "C6": "", "D6": "", "E6": "", "F6": "", "G6": "", "H6": "", "I6": "",
        "Z5": "", "A5": "", "B5": "", "C5": "", "D5": "", "E5": "", "F5": "", "G5": "", "H5": "", "I5": "",
        "Z4": "", "A4": "", "B4": "", "C4": "", "D4": "", "E4": "", "F4": "", "G4": "", "H4": "", "I4": "",
        "Z3": "", "A3": "", "B3": "", "C3": "", "D3": "", "E3": "", "F3": "", "G3": "", "H3": "", "I3": "",
        "Z2": "", "A2": "P", "B2": "P", "C2": "P", "D2": "P", "E2": "P", "F2": "P", "G2": "P", "H2": "P", "I2": "",
        "Z1": "", "A1": "R", "B1": "K", "C1": "B", "D1": "Q", "E1": "I", "F1": "B", "G1": "K", "H1": "R", "I1": "",
        "Z0": "", "A0": "", "B0": "", "C0": "", "D0": "", "E0": "", "F0": "", "G0": "", "H0": "", "I0": ""
    }
    return board
