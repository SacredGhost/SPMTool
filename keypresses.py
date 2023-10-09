import ctypes
from ctypes import wintypes
import time
user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def PressRelease(hexKeyCode, duration_ms):
    PressKey(hexKeyCode)
    time.sleep(duration_ms/1000)
    ReleaseKey(hexKeyCode)
    
def toKeyCode(c):
    keyCode = keyCodeMap[c]
    return keyCode

keyCodeMap = {
    'left'              : 0x4B,
    'down'              : 0x0A,
    'shift'             : 0x10,
    '0'                 : 0x30,
    '1'                 : 0x31,
    '2'                 : 0x32,
    '3'                 : 0x33,
    '4'                 : 0x34,
    '5'                 : 0x35,
    '6'                 : 0x36,
    '7'                 : 0x37,
    '8'                 : 0x38,
    '9'                 : 0x39,
    'a'                 : 0x41,
    'b'                 : 0x42,
    'c'                 : 0x43,
    'd'                 : 0x44,
    'e'                 : 0x45,
    'f'                 : 0x46,
    'g'                 : 0x47,
    'h'                 : 0x48,
    'up'                : 0x49,
    'left'              : 0x4A,
    'down'              : 0x4B,
    'right'             : 0x4C,
    '+'                 : 0x4D,
    '-'                 : 0x4E,
    'o'                 : 0x4F,
    'p'                 : 0x50,
    'q'                 : 0x51,
    'r'                 : 0x52,
    's'                 : 0x53,
    't'                 : 0x54,
    'u'                 : 0x55,
    'v'                 : 0x56,
    'w'                 : 0x57,
    'x'                 : 0x58,
    'y'                 : 0x59,
    'z'                 : 0x5A,
    'num0'              : 0x60,
    'num1'              : 0x61,
    'num2'              : 0x62,
    'num3'              : 0x63,
    'num4'              : 0x64,
    'num5'              : 0x65,
    'num6'              : 0x66,
    'num7'              : 0x67,
    'num8'              : 0x68,
    'num9'              : 0x69,
    '+'                 : 0x6B,
    '-'                 : 0x6D,
    '*'                 : 0x6A,
    '/'                 : 0x6F,
    '.'                 : 0x6E,
}