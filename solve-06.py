# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 06: Guard Gallivant ---"
  input = "input-06.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def startPos(lines):
  for y, l in enumerate(lines):
    sp = l.find("^")
    if sp != -1:
      return (sp, y)
  return None

def move(p, dir):
  return (p[0] + dir[0], p[1] + dir[1])

def inBox(p, maxP):
  x, y = p
  return x >=0 and x < maxP[0] and y >= 0 and y < maxP[0]

def getVisits(lines):
  p = startPos(lines)
  maxP = (len(lines[0]), len(lines))
  dir = (0, -1)
  turnRight = {(0, -1) : (1, 0), (1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1)}
  visits = set([p])
  while True:
    np = move(p, dir)
    if not inBox(np, maxP):
      break
    nx, ny = np
    if lines[ny][nx] == "#":
      dir = turnRight[dir]
    else:
      p = np
      visits.add(p)
  return visits

def solve1(lines):
  visits = getVisits(lines)
  print("Solution 1: ", len(visits))

def tryObstruction(op, lines):
  p = startPos(lines)
  maxP = (len(lines[0]), len(lines))
  dir = (0, -1)
  turnRight = {(0, -1) : (1, 0), (1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1)}
  visits = set([(p, dir)])
  while True:
    np = move(p, dir)
    if not inBox(np, maxP):
      break
    nx, ny = np
    if np == op or lines[ny][nx] == "#":
      dir = turnRight[dir]
    else:
      p = np
      if (p, dir) in visits:
        return True
      visits.add((p, dir))
  return False

def solve2(lines):
  no = 0
  for v in getVisits(lines):
    if tryObstruction(v, lines):
      no += 1
  print("Solution 2: ", no)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
