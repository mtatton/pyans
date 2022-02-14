#!/usr/bin/python3
# 
# (c) Shinobi MMXXII
#
# https://asciinema.org/a/tZHWD8zyQlNUKRfhyHTkpZ7iP
#

import os
import sys
import curses
import signal
from time import sleep

# conversion matrix to utf8
cmatu=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,199,252,233,226,228,224,229,231,234,235,232,239,238,236,196,197,201,230,198,244,246,242,251,249,255,214,220,162,163,165,8359,402,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,223,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]

def handler(signum, frame):
  curses.endwin()
  exit()

signal.signal(signal.SIGINT, handler)

def prn(pstr):
  global prn_cy
  scr.move(prn_cy,2)
  scr.addstr(pstr)
  prn_cy+=1

# print the sauce information
def prn_help():
  global prn_cy
  prn_cy = 3
  #cols = str(int.from_bytes(pos_sauce[96:98],"little"))
  #rows = (int.from_bytes(pos_sauce[98:100],"little"))
  prn(r" __________                               ")
  prn(r" \______   \___.__._____    ____   ______ ")
  prn(r"  |     ___<   |  |\__  \  /    \ /  ___/ ")
  prn(r"  |    |    \___  | / __ \|   |  \\___ \  ")
  prn(r"  |____|    / ____|(____  /___|  /____  > ")
  prn(r"            \/          \/     \/     \/  ")
  prn(r"       /-|                             |- ")
  prn(r"  -.'.'.-|  Python Console ANSI Viewer |- ")
  prn(r"       \-|                             |- ")
  prn(r"")
  prn(r"   u, n       - scroll up, down more         ")
  prn(r"   k, j, h, l - scroll up, down, left, right ")
  prn(r"   $          - display sauce information    ")
  prn(r"   ?          - display help                 ")
  prn(r"   a          - autoscroll                   ")
  prn(r"")


# print the sauce information
def prn_sauce_info(pos_sauce):
  global prn_cy
  prn_cy = 2
  #cols = str(int.from_bytes(pos_sauce[96:98],"little"))
  #rows = (int.from_bytes(pos_sauce[98:100],"little"))
  prn("Title : "+pos_sauce[7:42].decode("utf8"))
  prn("Author: "+pos_sauce[42:62].decode("utf8"))
  prn("Group : "+pos_sauce[62:82].decode("utf8"))
  prn("Date  : "+pos_sauce[82:90].decode("utf8"))
  prn("FSize : "+str(int.from_bytes(pos_sauce[90:94],"little")))
  prn("DType : "+str(int.from_bytes(pos_sauce[94:95],"little")))
  prn("FType : "+str(int.from_bytes(pos_sauce[95:96],"little")))
  prn("TInf1 : "+str(int.from_bytes(pos_sauce[96:98],"little")))
  prn("TInf2 : "+str(int.from_bytes(pos_sauce[98:100],"little")))
  prn("TInf3 : "+str(int.from_bytes(pos_sauce[100:102],"little")))
  prn("TInf4 : "+str(int.from_bytes(pos_sauce[102:104],"little")))
  prn("ComLn : "+str(int.from_bytes(pos_sauce[104:105],"little")))


def cls(he):
  scr.move(0,0)
  cy=0
  for cy in range(0,he):
    scr.move(0,0)
    scr.clrtoeol()

# translate our color code to curses colors
def curs_col(scol):
  if scol == "Bk":
    rc = curses.COLOR_BLACK
  elif scol == "Re":
    rc = curses.COLOR_RED
  elif scol == "Gr":
    rc = curses.COLOR_GREEN
  elif scol == "Ye":
    rc = curses.COLOR_YELLOW
  elif scol == "Ma":
    rc = curses.COLOR_MAGENTA
  elif scol == "Bl":
    rc = curses.COLOR_BLUE
  elif scol == "Cy":
    rc = curses.COLOR_CYAN
  elif scol == "Wh":
    rc = curses.COLOR_WHITE
  return(rc)

# get the two chars color code
def get_col(iattr):
  mia = iattr % 10
  if   mia == 0: col = "Bk"
  elif mia == 1: col = "Re"
  elif mia == 2: col = "Gr"
  elif mia == 3: col = "Ye"
  elif mia == 4: col = "Bl"
  elif mia == 5: col = "Ma"
  elif mia == 6: col = "Cy"
  elif mia == 7: col = "Wh"
  return(col)

# init curses color based on foreground, background and attribute
def init_cur_clr(fg,bg,attr):
  global clrs
  global max_colors
  max_colors+=1
  cfg = curs_col(fg)
  cbg = curs_col(bg)
  curses.init_pair(max_colors, cfg, cbg)
  if attr == "hi":
    clrs[attr+fg+bg] = curses.color_pair(max_colors) | curses.A_BOLD
  elif attr == "lo":
    clrs[attr+fg+bg] = curses.color_pair(max_colors) | curses.A_DIM
  #elif attr == "hb":
  #  clrs[attr+fg+bg] = curses.color_pair(max_colors) | curses.REVERSE 
  else:
    clrs[attr+fg+bg] = curses.color_pair(max_colors)

def render_ans(pad, ans, width=80, height=25, shift_y=0):
  # display ans variables
  cx = 0
  cy = 0
  # escape sequence state
  stat = ""
  attr = ""
  inten = "me"
  fgcol = "Wh"
  bgcol = "Bk"
  curcol = "meWhBk"
  lp = 0 # last printed row
  # main ansi loop
  for c in ans:
    # from this point there could be SAUCE
    #if c == 0x1a:
    #  break
    # new line move to new line
    if c == ord("\n"):
      cy += 1
      continue
    # linefeed go to first column
    elif c == ord("\r"):
      cx = 0
      continue
    # set state to start of escape sequence
    elif c == 27:
      stat = "E"
      continue  
    # set state to graphical escape sequence
    if stat == "E":
      if c == ord("["):
        stat = "ES"
        continue
    # graphical escape sequence
    elif stat == "ES":
      # cursor movement escape sequence
      if c == ord("C"):
        ia = int(attr)
        cx+=ia
        attr=""
        stat=""
        continue
      # read escape character numeric attribute
      elif c >= ord("0") and c <= ord("9"):
        attr += chr(c)
        continue
      # escape character terminator
      elif c == ord(";") or c == ord("m"):
        # get integer attribute
        ia = int(attr)
        # reset color to default
        if ia == 0:
          inten = "me"
          fgcol = "Wh"
          bgcol = "Bk"
        # hight intensity attribute
        elif ia == 1:
          inten = "hi" 
        # foreground colors
        elif (ia >= 30 and ia <= 37) or (ia >= 90 and ia <= 97):
          fgcol = get_col(ia)
        # background colors
        elif (ia >= 40 and ia <= 47) or (ia >= 100 and ia <= 107):
          bgcol = get_col(ia)
        # get current color code
        curcol = inten + fgcol + bgcol
        # initialize the color if it isn't not ready
        if curcol not in clrs:
          init_cur_clr(fgcol,bgcol,inten)
        # debug
        #pad.addstr(cy,int(cx*2)+80,str(ia),clrs[curcol])
        attr=""
        # reset escape sequence state
        if c == ord("m"):
          stat = ""
        continue
    # some ansi's assume we will handle end of line
    if cx >= width:
      cy+=1 
      cx=0
    try:
      pad.addstr(cy,cx,chr(cmatu[c]),clrs[curcol])
      cx+=1
    except Exception as e:
      # debug
      #ocx=cx
      #ocy=cy
      #scr.move(he-1,0)
      #scr.addstr(str(e)+" "+str(cy)+" "+str(cx))
      #scr.move(ocy,ocy)
      #scr.getch()
      pass
  #scr.move(0,0)
  #prn(str(shift_y) + " " + sys.argv[1],"hiWhBk")
  return(cy)

# process the command line arguments
if len(sys.argv) != 2:
  print("-| python curses ansi graphic viewer |-")
  print("Usage: "+sys.argv[0]+" <ansi file>")
  exit()

# more variables
clrs = {}
max_colors = 1
prn_cy = 0
dans = ""

fname = sys.argv[1]
# try to read the file
if os.path.exists(fname):
  try:
    # read the ans as binary
    f = open(fname,"rb")
    dans = f.read()
    f.close()
  except:
    print("Can't open specified file")
    # make the compiler happy
    exit(0) 
else:
  # file provided is not there 
  print("The file doesn't exists")
  exit(0) 

# default sauce variables
cols = 80
rows = 25
sauce_info = ""
# try to process souce
pos_sauce = dans[-128:]
# check for sauce existance
if pos_sauce[:5]==b'SAUCE':
  #print("Confirmed")
  # check if sauce version is 00
  if pos_sauce[5:7]==b'00':
    # get sauce width and height
    cols = int.from_bytes(pos_sauce[96:98],"little")
    rows = int.from_bytes(pos_sauce[98:100],"little")
    # cut sauce from data
    dans = dans[:-129]

# variables
k="0"
cli = 0
shift_y = 0
shift_x = 0
autoscroll = 0
# init curses
scr = curses.initscr()
#scr.getch()
# we want colors
curses.start_color()
# no new lines
curses.nonl()
# no echoing of keypresses
curses.noecho()
# get screen size
he, wi = scr.getmaxyx()
# hide the cursor
curses.curs_set(0)
# prepare new curses pad
pad = curses.newpad(rows, cols*4) # lines, cols
cli = render_ans(pad,dans,cols,rows,shift_y)
# screen size variables
while k != ord("q"):
  he, wi = scr.getmaxyx()
  he -= 1
  wi = cols
  # scroll up more
  if k == ord("u"):
    if shift_y - 10 > 0:
      shift_y -= 10
    else:
      shift_y = 0
  # scroll down more
  if k == ord("n"):
    if shift_y + 10 < cli - he - 1:
      shift_y += 10
    else:
      shift_y = cli - he
  # scroll down
  elif k == ord("j"):
    if shift_y < cli - he -1:
      shift_y += 1
  # scroll up
  elif k == ord("k"):
    if shift_y > 0:
      shift_y -= 1
  # scroll left
  elif k == ord("h"):
    if shift_x > 0:
      shift_x -= 1
  # scroll right
  elif k == ord("l"):
    if shift_x < wi-1:
      shift_x += 1
  # display basic sauce information
  elif k == ord("$"):
    cls(he)
    prn_sauce_info(pos_sauce)
    scr.getch()
  # display help
  elif k == ord("?"):
    cls(he)
    prn_help()
    scr.getch()
  # autoscroll
  elif k == ord("a"):
    # if not turned on
    if autoscroll == 0:
      autoscroll = 1
      # set timeout for getch
      scr.timeout(100)
    # if turned on
    elif autoscroll == 1:
      autoscroll = 0
      # set no timeout for getch
      scr.timeout(0)
  scr.refresh()
  pad.refresh(0+shift_y,0+shift_x, 0,0, he,wi-1)
  # main autoscroll routine
  if autoscroll == 1:
    if shift_y < cli - he - 1:
      shift_y += 1
    else:
      autoscroll = 0
  # wait for key press
  k = scr.getch()
# show the cursor
curses.curs_set(2)
# turn on new line
curses.nl()
# turn on keys echoing
curses.echo()
# end the curses
curses.endwin()

