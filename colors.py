# -*- coding: utf-8 -*-
import platform
import ctypes
red = "\033[21;31m"
green = "\033[21;32m"
yellow = "\033[21;33m"
blue = "\033[21;34m"
normal = "\033[0m"
purple = "\033[21;35m"
cyan = "\033[21;36m"
def w32setcolor(color):
  std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
  ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, color)
def loaded(t):
  if platform.system() == "Linux":
    print blue+" [LOADED] "+t+normal
  else:
    w32setcolor(0x02)
    print " [LOADED] "+t
    w32setcolor(0x07)
def reloaded(t):
  if platform.system() == "Linux":
    print purple+" [RELOADED] "+t+normal
  else:
    w32setcolor(0x02)
    print " [RELOADED] "+t
    w32setcolor(0x07)
def notice(t):
  if platform.system() == "Linux":
    print cyan+" [NOTICE] "+t+normal
  else:
    w32setcolor(0x02|0x08)
    print " [NOTICE] "+t
    w32setcolor(0x07)
def error(t):
  if platform.system() == "Linux":
    print red+" [ERROR ] "+t+normal
  else:
    w32setcolor(0x04|0x08)
    print " [ERROR ] "+t
    w32setcolor(0x07)
def good(t):
  if platform.system() == "Linux":
    print green+" [ GOOD ] "+t+normal
  else:
    w32setcolor(0x01|0x08)
    print " [ GOOD ] "+t
    w32setcolor(0x07)
def bad(t):
  if platform.system() == "Linux":
    print yellow+" [ BAD  ] "+t+normal
  else:
    w32setcolor(0x18)
    print " [ BAD ] "+t
    w32setcolor(0x07)
