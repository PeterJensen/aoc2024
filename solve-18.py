# Author: Peter Jensen

import sys
import djikstra

class Config:
  title = "--- Day 18: RAM Run ---"
  input = "input-18.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Node:
  dirs = [(0,-1), (1,0), (0,1), (-1,0)]
  dims = (7, 7)
  corrupted = set()
  def __init__(self, pos):
    self.pos = pos
    self.match = self.__eq__
  def __repr__(self):
    return f"{self.pos}"
  def __eq__(self, other):
    return self.pos == other.pos
  def __hash__(self):
    return hash(self.pos)
  @classmethod
  def move(cls, pos, dir):
    xd, yd = dir
    return (pos[0] + xd, pos[1] + yd)
  def neighbors(self):
    for d in self.dirs:
      n = self.move(self.pos, d)
      x, y = n
      if x >=0 and x < self.dims[0] and y >= 0 and y < self.dims[1] and n not in self.corrupted:
        yield Node(n)

def getCorrupted(lines, n):
  corrupted = []
  for li, l in enumerate(lines):
    if n != None and li == n:
      break
    corrupted.append(tuple(map(int, l.split(","))))
  return corrupted

def solve1(lines):
  Node.corrupted = getCorrupted(lines, 1024)
  dims = (71, 71)
  Node.dims = dims
  startNode = Node((0, 0))
  endNode   = Node((dims[0]-1, dims[1]-1))
  dist, prev = djikstra.shortest(startNode, endNode)
  print("Solution 1: ", dist[endNode])

def solve2(lines):
  corrupted = getCorrupted(lines, None)
  dims = (71, 71)
  Node.dims = dims
  startNode = Node((0, 0))
  endNode   = Node((dims[0]-1, dims[1]-1))
  for n in range(2896, len(corrupted)):
    Node.corrupted = corrupted[0:n+1]
    dist, prev = djikstra.shortest(startNode, endNode)
#    print(f"{n}: {corrupted[n]} {dist[endNode]}")
    if dist[endNode] == 999999999:
      break
  print("Solution 2: ", corrupted[n])
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
