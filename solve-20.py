# Author: Peter Jensen

import sys
import djikstra
import itertools

class Config:
  title = "--- Day 20: Race Condition ---"
  input = "input-20.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Grid:
  def __init__(self, lines):
    self.lines = lines
    self.dims = (len(lines[0]), len(lines))
    self.cheat = None
    for y, l in enumerate(lines):
      for x, c in enumerate(l):
        if c == "S":
          self.start = (x, y)
        elif c == "E":
          self.end = (x, y)
  def setCheat(self, cheat):
    self.cheat = cheat
  def get(self, pos):
    x, y = pos
    if x < 0 or x >= self.dims[0] or y < 0 or y >= self.dims[1]:
      return "#"
    elif self.cheat != None and pos == self.cheat:
      return "."
    else:
      c = self.lines[y][x]
      return "." if c in ".SE" else "#"
  def isValidCheat(self, cheat):
#    return self.get(cheat) == "#"
    x, y = cheat
    return self.get(cheat) == "#" and ((self.get((x-1, y)) == "." and self.get((x+1, y)) == ".") or (self.get((x, y-1)) == "." and self.get((x, y+1)) == "."))
  def allCheats(self):
    for y in range(1, self.dims[1]-1):
      for x in range(1, self.dims[0]-1):
        if self.isValidCheat((x, y)):
          yield (x, y)

class Node:
  grid = None
  dirs = [(-1,0), (1,0), (0,-1), (0,1)]
  def __init__(self, pos):
    self.pos = pos
    self.match = self.__eq__
  def __repr__(self):
    return f"{self.pos}"
  def __eq__(self, other):
    return self.pos == other.pos
  def __hash__(self):
    return hash(self.pos)
  def manhatten(self, other):
    sx, sy = self.pos
    ox, oy = other.pos
    return abs(sx - ox) + abs(sy - oy)
  @staticmethod
  def move(pos, dir):
    x, y   = pos
    xd, yd = dir
    return (x + xd, y + yd)
  def neighbors(self):
    for d in self.dirs:
      np = self.move(self.pos, d)
      if self.grid.get(np) == ".":
        yield Node(np)

def getDistWithCheat(grid, start, end, cheat):
  grid.setCheat(cheat)
  Node.grid = grid
  startNode, endNode = Node(start), Node(end)
  dist, prev = djikstra.shortest(startNode, endNode)
  return dist[endNode]

def cheatSaving(grid, cheat):
  x, y = cheat
  x1, x2 = (x-1, y), (x+1, y)
  if grid.get(x1) == "." and grid.get(x2) == ".":
    return getDistWithCheat(grid, x1, x2, None) - 2
  y1, y2 = (x, y-1), (x, y+1)
  if grid.get(y1) == "." and grid.get(y2) == ".":
    return getDistWithCheat(grid, y1, y2, None) - 2
  
def solve1(lines):
  grid = Grid(lines)
  cheat100Count = 0
  for ci, cheat in enumerate(grid.allCheats()):
    saving = cheatSaving(grid, cheat)
    if saving >= 100:
      cheat100Count += 1
  print("Solution 1: ", cheat100Count)

def solve2(lines):
  grid = Grid(lines)
  Node.grid = grid
  startNode, endNode = Node(grid.start), Node(grid.end)
  dist, prev = djikstra.shortest(startNode, endNode)

  c = 0
  for p1, p2 in itertools.combinations(itertools.chain([startNode], prev.keys()), 2):
    d = abs(dist[p1] - dist[p2])
    md = p1.manhatten(p2)
    if md < 21 and (d - md) >= 100:
      c += 1
#      print(f"{p1} - {p2}")
  print("Solution 2: ", c)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
