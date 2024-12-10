# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 10: Hoof It ---"
  input = "input-10.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def getHeads(lines):
  heads = []
  for y, l in enumerate(lines):
    for x, c in enumerate(l):
      if lines[y][x] == "0":
        heads.append((x, y))
  return heads

def nextHeads(head, lines):
  xh, yh = head
  hv = int(lines[yh][xh])
  for x, y in [(xh - 1, yh), (xh + 1, yh), (xh, yh - 1), (xh, yh + 1)]:
    if x >= 0 and x < len(lines[0]) and y >= 0 and y < len(lines):
      nv = lines[y][x]
      if nv != "." and int(nv) == hv + 1:
        yield (x, y)

def trailCount(head, lines, ends):
  xh, yh = head
  hv = int(lines[yh][xh])
  if hv == 9:
    if not head in ends:
      ends.append(head)
      return 1
    else:
      return 0
  numHeads = 0
  for nh in nextHeads(head, lines):
    numHeads += trailCount(nh, lines, ends)
  return numHeads

def solve1(lines):
  heads = getHeads(lines)
  numTrails = 0
  for h in heads:
    numTrails += trailCount(h, lines, [])
  print("Solution 1: ", numTrails)

def trailRating(head, lines):
  xh, yh = head
  hv = int(lines[yh][xh])
  if hv == 9:
    return 1
  rating = 0
  for nh in nextHeads(head, lines):
    rating += trailRating(nh, lines)
  return rating

def solve2(lines):
  heads = getHeads(lines)
  rating = 0
  for h in heads:
    rating += trailRating(h, lines)
  print("Solution 2: ", rating)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
