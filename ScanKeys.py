from typing import Union


class Key:
    def __init__(self, key: Union[str, int, hex]):
        self.key = key if isinstance(key, str) else get_key(key)
        self.scancode = get_code(self.key)

    def __repr__(self):
        return f"Key: {self.key}, ScanCode: {self.scancode}"


def get_key(code: Union[int, hex]) -> str:
    try:
        return ScanKeys[code if isinstance(code, int) else int(code)]
    except IndexError:
        raise ValueError(f"Code: {code} is don`t exists")


def get_code(key: str) -> int:
    try:
        return [code[0] for code in ScanKeys.items() if key.lower() == code[1].lower()][0]
    except KeyError:
        raise ValueError(f"Key: {key} is don`t exists")


ScanKeys = {
    1: "Esc",
    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "0",
    12: "-",
    13: "+",
    14: "Backspace",
    15: "Tab",
    16: "Q",
    17: "W",
    18: "E",
    19: "R",
    20: "T",
    21: "Y",
    22: "U",
    23: "I",
    24: "O",
    25: "P",
    26: "[",
    27: "]",
    28: "Enter",
    29: "LeftControl",
    30: "A",
    31: "S",
    32: "D",
    33: "F",
    34: "G",
    35: "H",
    36: "J",
    37: "K",
    38: "L",
    39: ";",
    40: "'",
    41: "~",
    42: "LeftShift",
    43: "\\",
    44: "Z",
    45: "X",
    46: "C",
    47: "V",
    48: "B",
    49: "N",
    50: "M",
    51: ",",
    52: ".",
    53: "/",
    54: "RightShift",
    55: "Numpad *",
    56: "LeftAlt",
    57: "Space",
    58: "CapsLock",
    59: "F1",
    60: "F2",
    61: "F3",
    62: "F4",
    63: "F5",
    64: "F6",
    65: "F7",
    66: "F8",
    67: "F9",
    68: "F10",
    69: "NumLock",
    70: "ScrollLock",
    71: "Numpad 7",
    72: "Numpad 8",
    73: "Numpad 9",
    74: "Numpad -",
    75: "Numpad 4",
    76: "Numpad 5",
    77: "Numpad 6",
    78: "Numpad +",
    79: "Numpad 1",
    80: "Numpad 2",
    81: "Numpad 3",
    82: "Numpad 0",
    83: "Numpad .",
    87: "F11",
    88: "F12",
    284: "NumpadEnter",
    285: "RightCtrl",
    309: "Numpad /",
    312: "RightAlt",
    325: "NumpadLock",
    327: "Home",
    328: "UpArrow",
    329: "PageUp",
    331: "LeftArrow",
    333: "RightArrow",
    335: "End",
    336: "DownArrow",
    337: "PageDown",
    338: "Insert",
    339: "Delete",
    347: "Win",
}
if __name__ == '__main__':
    print(get_code("Insert"))
    print(get_key(17))

    key = Key(33)
    print(key)