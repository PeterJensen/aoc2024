# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 25: Code Chronicle ---"
  input = "input-25.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def parse(lines):
  locks = []
  keys = []
  isStart = True
  for li in range(0, len(lines), 8):
    lk = lines[li:li+7]
    if lk[0] == "#####":
      si = 1
    else:
      si = 0
    combo = [0 for _ in range(5)]
    for l in lk[si:si+6]:
      for ci, c in enumerate(l):
        if c == "#":
          combo[ci] += 1
    if si == 1:
      locks.append(combo)
    else:
      keys.append(combo)
  return locks, keys

def fits(lock, key):
  for i in range(5):
    if lock[i] + key[i] > 5:
      return False
  return True

def solve1(lines):
  locks, keys = parse(lines)
  numPairs = 0
  for l,k in itertools.product(locks, keys):
    if fits(l, k):
      numPairs += 1
  print("Solution 1: ", numPairs)

def solve2(lines):
  print("Solution 2: ")
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
