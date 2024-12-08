# Author: Peter Jensen

import sys
from collections import defaultdict
import itertools

class Config:
  title = "--- Day 08: Resonant Collinearity ---"
  input = "input-08.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def parse(lines):
  antennas = defaultdict()
  for y,l in enumerate(lines):
    for x, c in enumerate(l):
      if c != ".":
        antennas.setdefault(c, set()).add((x, y))
  return antennas, (len(lines[0]) - 1, len(lines)-1)

def inBox(p, maxP):
  x, y = p
  xm, ym = maxP
  return x >= 0 and x <= xm and y >= 0 and y <= ym

def getAntiNodes1(a1, a2, maxP):
  x1, y1 = a1
  x2, y2 = a2
  xd = x1 - x2
  yd = y1 - y2
  an1 = (x1 + xd, y1 + yd)
  if inBox(an1, maxP):
    yield an1
  an2 = (x2 - xd, y2 - yd)
  if inBox(an2, maxP):
    yield an2

def getAntiNodes2(a1, a2, maxP):
  x1, y1 = a1
  x2, y2 = a2
  xd = x1 - x2
  yd = y1 - y2
  yield a1
  yield a2
  while True:
    an1 = (x1 + xd, y1 + yd)
    if inBox(an1, maxP):
      yield an1
      x1, y1 = an1
    else:
      break
  while True:
    an2 = (x2 - xd, y2 - yd)
    if inBox(an2, maxP):
      yield an2
      x2, y2 = an2
    else:
      break

def solve1(lines):
  allAntennas, maxP = parse(lines)
  antiNodes = set()
  for name, antennas in allAntennas.items():
    for a1, a2 in itertools.combinations(antennas, 2):
      for an in getAntiNodes1(a1, a2, maxP):
        antiNodes.add(an)
  print("Solution 1: ", len(antiNodes))

def solve2(lines):
  allAntennas, maxP = parse(lines)
  antiNodes = set()
  for name, antennas in allAntennas.items():
    for a1, a2 in itertools.combinations(antennas, 2):
      for an in getAntiNodes2(a1, a2, maxP):
        antiNodes.add(an)
  print("Solution 2: ", len(antiNodes))

def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
