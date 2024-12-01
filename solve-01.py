# Author: Peter Jensen

import sys
import re

class Config:
  title = "--- Day 01: Historian Hysteria ---"
  input = "input-01.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def getLists(lines):
  l1, l2 = [], []
  for l in lines:
    e1, e2 = re.split(r" +", l)
    l1.append(int(e1))
    l2.append(int(e2))
  return l1, l2

def solve1(lines):
  l1, l2 = getLists(lines)
  result = sum([abs(e1 - e2) for (e1, e2) in zip(sorted(l1), sorted(l2))])
  print("Solution 1: ", result)

def solve2(lines):
  l1, l2 = getLists(lines)
  result = sum([e*l2.count(e) for e in l1])
  print("Solution 2: ", result)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
