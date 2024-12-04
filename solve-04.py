# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 04: Ceres Search ---"
  input = "input-04.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def horizontals(lines):
  for l in lines:
    for x in range(0, len(l) - 3):
      yield l[x:x+4]

def verticals(lines):
  for y in range(0, len(lines) - 3):
    for x in range(len(lines[y])):
      yield lines[y][x] + lines[y+1][x] + lines[y+2][x] + lines[y+3][x]

def diags1(lines):
  for y in range(0, len(lines) - 3):
    for x in range(0, len(lines[y]) - 3):
      yield lines[y][x] + lines[y+1][x+1] + lines[y+2][x+2] + lines[y+3][x+3]

def diags2(lines):
  for y in range(0, len(lines) - 3):
    for x in range(3, len(lines[y])):
      yield lines[y][x] + lines[y+1][x-1] + lines[y+2][x-2] + lines[y+3][x-3]

def all(lines):
  for w in verticals(lines):
    yield w
  for w in horizontals(lines):
    yield w
  for w in diags1(lines):
    yield w
  for w in diags2(lines):
    yield w

def solve1(lines):
  wc = 0
  for w in all(lines):
    if w == "XMAS" or w == "SAMX":
      wc += 1
  print("Solution 1: ", wc)

def all3x3(lines):
  for y in range(0, len(lines) - 2):
    for x in range(0, len(lines[y]) - 2):
      yield [[lines[yi][xi] for xi in range(x, x + 3)] for yi in range(y, y + 3)]

def isX(sq):
  d1 = sq[0][0] + sq[1][1] + sq[2][2]
  d2 = sq[0][2] + sq[1][1] + sq[2][0]
  return (d1 == "MAS" or d1 == "SAM") and (d2 == "MAS" or d2 == "SAM")

def solve2(lines):
  xc = 0
  for sq in all3x3(lines):
    if isX(sq):
      xc += 1
  print("Solution 2: ", xc)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
