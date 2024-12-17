# Author: Peter Jensen

import sys
import djikstra

class Config:
  title = "--- Day 16: Reindeer Maze ---"
  input = "input-16.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Node:
  dirs = [(0,-1), (1,0), (0,1), (-1,0)]
  maze = None
  def __init__(self, pos, dir):
    self.pos = pos
    self.dir = dir
    self.match = self.__eq__
  def __repr__(self):
    return f"{self.pos}{self.dir}"
  def __eq__(self, other):
    dirOk = self.dir == None or other.dir == None or self.dir == other.dir
    return self.pos == other.pos and dirOk
  def __hash__(self):
    return hash(self.pos)
  def distTo(self, other):
    if self.pos == other.pos:
      return 1000
    else:
      return 1
  @classmethod
  def move(cls, pos, dir):
    xd, yd = cls.dirs[dir]
    return (pos[0] + xd, pos[1] + yd)
  def neighbors(self):
    yield Node(self.pos, (self.dir + 1) % 4)
    yield Node(self.pos, (self.dir - 1) % 4)
    np = self.move(self.pos, self.dir)
    if self.maze.isOpen(np):
      yield Node(np, self.dir)

class Maze:
  def __init__(self, lines):
    self.lines = lines
    self.dims  = (len(lines[0]), len(lines))
    for y,l in enumerate(lines):
      for x,c in enumerate(l):
        if c == "S":
          self.start = Node((x,y), 1)
        elif c == "E":
          self.end = Node((x,y), None)
  def __repr__(self):
    img = ""
    for l in self.lines:
      img += l + "\n"
    return img
  def imageWithOs(self, os):
    img = ""
    for y,l in enumerate(self.lines):
      for x,c in enumerate(l):
        if c == "#":
          img += c
        elif (x,y) in os:
          img += "O"
        else:
          img += "."
      img += "\n"
    return img

  def isOpen(self, pos):
    return self.lines[pos[1]][pos[0]] in ".E"

def solve1(lines):
  maze = Maze(lines)
  Node.maze = maze
  print(maze)
  dist, prev = djikstra.shortest(maze.start, maze.end)
  print("Solution 1: ", dist[maze.end])

def solve2(lines):
  maze = Maze(lines)
  Node.maze = maze
  os = set([maze.start.pos])
  dist, prev = djikstra.allShortest(maze.start, maze.end)
  worklist = [maze.end]
  while len(worklist) > 0:
    n = worklist.pop()
    if n.pos != maze.start.pos:
      os.add(n.pos)
      for p in prev[n]:
        worklist.append(p)
  print(maze.imageWithOs(os))
  print("Solution 2: ", len(os))
  
def main():
  print(Config.title)
  lines = getLines()
#  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
