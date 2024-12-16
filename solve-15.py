# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 15: Warehouse Woes ---"
  input = "input-15.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Grid:
  def __init__(self, lines):
    self.walls = set()
    self.boxes = set()
    self.robot = None
    self.dims  = None
    for y, l in enumerate(lines):
      if l == "":
        self.dims = (len(lines[0]), y)
        return
      for x, c in enumerate(l):
        if c == "@":
          self.robot = (x,y)
        elif c == "O":
          self.boxes.add((x, y))
        elif c == "#":
          self.walls.add((x,y))
  def __repr__(self):
    img = ""
    for y in range(self.dims[1]):
      l = "".join(["#" if (x,y) in self.walls else "O" if (x,y) in self.boxes else "@" if (x,y) == self.robot else "." for x in range(self.dims[0])])
      img += l + "\n"
    return img

  dirsXY = {">": (1,0), "v": (0,1), "<": (-1,0), "^": (0,-1)}
  @classmethod  
  def next(cls, pos, dir):
    dirXY = cls.dirsXY[dir]
    return (pos[0] + dirXY[0], pos[1] + dirXY[1])

  def move(self, pos, dir):
    nextPos = self.next(pos, dir)
    if nextPos in self.walls:
      return None
    if nextPos not in self.boxes:
      return nextPos
    else:
      nb = self.move(nextPos, dir)
      if nb != None:
        self.boxes.remove(nextPos)
        self.boxes.add(nb)
        return nextPos
      else:
        return None

  def gpsSum(self):
    s = 0
    for b in self.boxes:
      if b == None:
        print("None found")
        return 0
      x, y = b
      s += y*100 + x
    return s

def parse(lines, GridClass):
  grid = GridClass(lines)
  moves = "".join(lines[grid.dims[1]+1:])
  return grid, moves

def solve1(lines):
  grid, moves = parse(lines, Grid)
  for m in moves:
    nextPos = grid.move(grid.robot, m)
    if nextPos != None:
      grid.robot = nextPos
  print("Solution 1: ", grid.gpsSum())

class Grid2(Grid):
  def __init__(self, lines):
    s = super()
    s.__init__(lines)
    self.walls = set([(x*2, y) for (x, y) in self.walls])
    self.boxes = set([(x*2, y) for (x, y) in self.boxes])
    self.robot = (self.robot[0]*2, self.robot[1])
  def __repr__(self):
    def markOf(p):
      x, y = p
      if (x,y) in self.walls or (x-1, y) in self.walls:
        return "#"
      elif (x,y) in self.boxes and (x+1, y) not in self.boxes:
        return "["
      elif (x-1,y) in self.boxes and (x, y) not in self.boxes:
        return "]"
      elif (x,y) == self.robot:
        return "@"
      else:
        return "."
    img = ""
    for y in range(self.dims[1]):
      l = "".join([markOf((x, y)) for x in range(2*self.dims[0])])
      img += l + "\n"
    return img
  def move(self, pos, dir):
    def inWall(pos):
      x, y = pos
      return pos in self.walls or (x-1, y) in self.walls
    def inBox(pos):
      x, y = pos
      return pos in self.boxes or (x-1, y) in self.boxes
    def boxPosPair(pos):
      x, y = pos
      if pos in self.boxes:
        return pos, (x+1, y)
      elif (x-1, y) in self.boxes:
        return (x-1, y), pos
      else:
        return pos, pos
    def canMove(pos, dir):
      np = self.next(pos, dir)
      if inWall(np):
        return False
      elif inBox(np):
        np1, np2 = boxPosPair(np)
        if dir == ">":
          return canMove(np2, dir)
        elif dir == "<":
          return canMove(np1, dir)
        else:
          return canMove(np1, dir) and canMove(np2, dir)
      else:
        return True
      
    nextPos = self.next(pos, dir)
    np1, np2 = boxPosPair(nextPos)
    if inWall(np1) or inWall(np2):
      return None
    if np1 == np2:
      # not in box
      return None if inWall(nextPos) else nextPos
    else:
      # in box
      if dir in "<":
        if canMove(np1, dir):
          nb = self.move(np1, dir)
          self.boxes.remove(np1)
          self.boxes.add(nb)
          return nextPos
        return None
      elif dir in ">":
        if canMove(np2, dir):
          nb = self.move(np2, dir)
          self.boxes.remove(np1)
          self.boxes.add(np2)
          return nextPos
        return None
      else: # dir in "^v"
        if canMove(np1, dir) and canMove(np2, dir):
          nb1 = self.move(np1, dir)
          nb2 = self.move(np2, dir)
          self.boxes.remove(np1)
          self.boxes.add(nb1)
          return nextPos
        return None

def solve2(lines):
  grid, moves = parse(lines, Grid2)
#  print(grid)
  for mi, m in enumerate(moves):
    nextPos = grid.move(grid.robot, m)
    if nextPos != None:
      grid.robot = nextPos
#  print(grid)
  print("Solution 2: ", grid.gpsSum())
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
