from enum import Enum

class KeyMod(Enum):
    NONE: int = 0
    LSHIFT: int = 1
    RSHIFT: int = 2
    SHIFT: int = 3
    LCTRL: int = 64
    RCTRL: int = 128
    CTRL: int = 192
    LALT: int = 256
    RALT: int = 512
    ALT: int = 768
    LMETA: int = 1024
    RMETA: int = 2048
    META: int = 2072
    CAPS: int = 8192
    NUM: int = 4096
    MODE: int = 16384

class Mods():
    def __init__(self, mods: int) -> None:
        self._mods: int = mods

    def has(self, mod: KeyMod) -> bool:
        return bool(self._mods & mod.value)
    
    def __str__(self) -> str:
        return f"Mods({', '.join([str(mod) for mod in KeyMod if self.has(mod)])})"

class Key():
    KEY_BACKSPACE: int = 8
    KEY_TAB: int = 9
    KEY_CLEAR: int = 1073741980
    KEY_RETURN: int = 13
    KEY_PAUSE: int = 1073741896
    KEY_ESCAPE: int = 27
    KEY_SPACE: int = 32
    KEY_EXCLAIM: int = 33
    KEY_QUOTEDBL: int = 34
    KEY_HASH: int = 35
    KEY_DOLLAR: int = 36
    KEY_AMPERSAND: int = 38
    KEY_QUOTE: int = 39
    KEY_LEFTPAREN: int = 40
    KEY_RIGHTPAREN: int = 41
    KEY_ASTERISK: int = 42
    KEY_PLUS: int = 43
    KEY_COMMA: int = 44
    KEY_MINUS: int = 45
    KEY_PERIOD: int = 46
    KEY_SLASH: int = 47
    KEY_0: int = 48
    KEY_1: int = 49
    KEY_2: int = 50
    KEY_3: int = 51
    KEY_4: int = 52
    KEY_5: int = 53
    KEY_6: int = 54
    KEY_7: int = 55
    KEY_8: int = 56
    KEY_9: int = 57
    KEY_COLON: int = 58
    KEY_SEMICOLON: int = 59
    KEY_LESS: int = 60
    KEY_EQUALS: int = 61
    KEY_GREATER: int = 62
    KEY_QUESTION: int = 63
    KEY_AT: int = 64
    KEY_LEFTBRACKET: int = 91
    KEY_BACKSLASH: int = 92
    KEY_RIGHTBRACKET: int = 93
    KEY_CARET: int = 94
    KEY_UNDERSCORE: int = 95
    KEY_BACKQUOTE: int = 96
    KEY_A: int = 97
    KEY_B: int = 98
    KEY_C: int = 99
    KEY_D: int = 100
    KEY_E: int = 101
    KEY_F: int = 102
    KEY_G: int = 103
    KEY_H: int = 104
    KEY_I: int = 105
    KEY_J: int = 106
    KEY_K: int = 107
    KEY_L: int = 108
    KEY_M: int = 109
    KEY_N: int = 110
    KEY_O: int = 111
    KEY_P: int = 112
    KEY_Q: int = 113
    KEY_R: int = 114
    KEY_S: int = 115
    KEY_T: int = 116
    KEY_U: int = 117
    KEY_V: int = 118
    KEY_W: int = 119
    KEY_X: int = 120
    KEY_Y: int = 121
    KEY_Z: int = 122
    KEY_DELETE: int = 127
    KEY_KP0: int = 1073741922
    KEY_KP1: int = 1073741913
    KEY_KP2: int = 1073741914
    KEY_KP3: int = 1073741915
    KEY_KP4: int = 1073741916
    KEY_KP5: int = 1073741917
    KEY_KP6: int = 1073741918
    KEY_KP7: int = 1073741919
    KEY_KP8: int = 1073741920
    KEY_KP9: int = 1073741921
    KEY_KP_PERIOD: int = 1073741923
    KEY_KP_DIVIDE: int = 1073741908
    KEY_KP_MULTIPLY: int = 1073741909
    KEY_KP_MINUS: int = 1073741910
    KEY_KP_PLUS: int = 1073741911
    KEY_KP_ENTER: int = 1073741912
    KEY_KP_EQUALS: int = 1073741927
    KEY_UP: int = 1073741906
    KEY_DOWN: int = 1073741905
    KEY_RIGHT: int = 1073741903
    KEY_LEFT: int = 1073741904
    KEY_INSERT: int = 1073741897
    KEY_HOME: int = 1073741898
    KEY_END: int = 1073741901
    KEY_PAGEUP: int = 1073741899
    KEY_PAGEDOWN: int = 1073741902
    KEY_F1: int = 1073741882
    KEY_F2: int = 1073741883
    KEY_F3: int = 1073741884
    KEY_F4: int = 1073741885
    KEY_F5: int = 1073741886
    KEY_F6: int = 1073741887
    KEY_F7: int = 1073741888
    KEY_F8: int = 1073741889
    KEY_F9: int = 1073741890
    KEY_F10: int = 1073741891
    KEY_F11: int = 1073741892
    KEY_F12: int = 1073741893
    KEY_F13: int = 1073741928
    KEY_F14: int = 1073741929
    KEY_F15: int = 1073741930
    KEY_NUMLOCK: int = 1073741907
    KEY_CAPSLOCK: int = 1073741881
    KEY_SCROLLOCK: int = 1073741895
    KEY_RSHIFT: int = 1073742053
    KEY_LSHIFT: int = 1073742049
    KEY_RCTRL: int = 1073742052
    KEY_LCTRL: int = 1073742048
    KEY_RALT: int = 1073742054
    KEY_LALT: int = 1073742050
    KEY_RMETA: int = 1073742055
    KEY_LMETA: int = 1073742051
    KEY_LSUPER: int = 1073742051
    KEY_RSUPER: int = 1073742055
    KEY_MODE: int = 1073742081
    KEY_HELP: int = 1073741941
    KEY_PRINT: int = 1073741894
    KEY_SYSREQ: int = 1073741978
    KEY_BREAK: int = 1073741896
    KEY_MENU: int = 1073741942
    KEY_POWER: int = 1073741926
    KEY_EURO: int = 1073742004
    
    def __init__(self, code: int, scancode: int, unicode: str, mods: Mods) -> None:
        self._code: int = code
        self._scancode: int = scancode
        self._unicode: str = unicode
        self._mods: Mods = mods
    
    @property
    def code(self) -> int:
        return self._code
    
    @property
    def scancode(self) -> int:
        return self._scancode
    
    @property
    def unicode(self) -> str:
        return self._unicode
    
    @property
    def mods(self) -> Mods:
        return self._mods
    
    def __str__(self) -> str:
        return f"Key(code = {self._code}, scancode = {self._scancode}, unicode = '{self._unicode}', mods = {self._mods})"
    
# chars = "abcdefghijklmnopqrstuvwxyz0123456789"
# special_chars = {
#     "`": "backtick",
#     "~": "tilde",
#     "!": "exclamation",
#     "@": "at",
#     "#": "hashtag",
#     "$": "dollar",
#     "%": "percent",
#     "^": "caret",
#     "&": "ampersand",
#     "*": "asterisk",
#     "(": "lparen",
#     ")": "rparen",
#     "_": "underscore",
#     "-": "hyphen",
#     "=": "equal",
#     "+": "plus",
#     "{": "lbracket",
#     "}": "rbracket",
#     "[": "lsquare",
#     "]": "rsquare",
#     "\\": "backslash",
#     "|": "pipe",
#     ":": "colon",
#     ";": "semicolon",
#     "'": "quote",
#     "\"": "dquote",
#     "<": "lt",
#     ",": "comma",
#     ">": "gt",
#     ".": "dot",
#     "/": "slash",
#     "?": "question"
# }

# for char in chars:
#     code = ord(char)

#     print(f"KEY_{char.upper()}: int = {code}")

# for char in special_chars:
#     code = ord(char)

#     print(f"KEY_{special_chars[char].upper()}: int = {code}")