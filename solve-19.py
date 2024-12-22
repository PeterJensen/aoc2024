# Author: Peter Jensen

import sys
import djikstra

class Config:
  title = "--- Day 19: Linen Layout ---"
  input = "input-19.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Node:
  towels = []
  def __init__(self, pattern):
    self.pattern = pattern
    self.match = self.__eq__
  def __repr__(self):
    return f"{self.pattern}"
  def __eq__(self, other):
    return self.pattern == other.pattern
  def __hash__(self):
    return hash(self.pattern)
  def neighbors(self):
    for t in self.towels:
      if self.pattern.find(t) == 0:
        yield Node(self.pattern[len(t):])

def parse(lines):
  return lines[0].split(", "), lines[2:]

def solve1(lines):
  towels, patterns = parse(lines)
  Node.towels = towels
  count = 0
  for p in patterns:
    startNode = Node(p)
    endNode = Node("")
    dist, prev = djikstra.shortest(startNode, endNode)
    if dist[endNode] != 999999999:
      count += 1
  print("Solution 1: ", count)

def numCombos(node, cache):
  if node.pattern == "":
    return 1
  if node in cache.keys():
    return cache[node]
  comboCount = 0
  for nn in node.neighbors():
    comboCount += numCombos(nn, cache)
  cache[node] = comboCount
  return comboCount

def solve2(lines):
  towels, patterns = parse(lines)
  Node.towels = towels
  count = 0
  for p in patterns:
    startNode = Node(p)
    c = numCombos(startNode, {})
#    print(f"pattern: {p} ", c)
    count += c
  print("Solution 2: ", count)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
