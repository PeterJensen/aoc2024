# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 12: Garden Groups ---"
  input = "input-12.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def neighborsOfSameKind(p, lines):
  x, y = p
  k = lines[y][x]
  xl, yl = len(lines[0]), len(lines)
  for xn, yn in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
    if xn >= 0 and xn < xl and yn >= 0 and yn < yl:
      if k == lines[yn][xn]:
        yield (xn, yn)

def inRegions(p, regions):
  for r in regions:
    if p in r:
      return True
  return False

def getRegion(start, lines):
  region = set()
  workList = [start]
  while len(workList) > 0:
    np = workList.pop()
    region.add(np)
    for n in neighborsOfSameKind(np, lines):
      if n not in region:
        region.add(n)
        workList.append(n)
  return region

def getRegions(lines):
  regions = []
  for y, l in enumerate(lines):
    for x, p in enumerate(l):
      pc = (x, y)
      if not inRegions(pc, regions):
        r = getRegion(pc, lines)
        regions.append(r)
  return regions

def fenceCount(p, lines):
  nk = 0
  for n in neighborsOfSameKind(p, lines):
    nk += 1
  return 4 - nk

def solve1(lines):
  regions = getRegions(lines)
  price = 0
  for r in regions:
    fence = 0
    for p in r:
      fence += fenceCount(p, lines)
    price += fence*len(r)
  print("Solution 1: ", price)

def numCorners(p, r):
  nc = 0
  x, y = p
  if (x+1, y) not in r and (x, y-1) not in r:
    nc += 1
  if (x+1, y) not in r and (x, y+1) not in r:
    nc += 1
  if (x, y+1) not in r and (x-1, y) not in r:
    nc += 1
  if (x-1, y) not in r and (x, y-1) not in r:
    nc += 1

  if (x+1, y) in r and (x, y-1) in r and (x+1, y-1) not in r:
    nc += 1
  if (x+1, y) in r and (x, y+1) in r and (x+1, y+1) not in r:
    nc += 1
  if (x, y+1) in r and (x-1, y) in r and (x-1, y+1) not in r:
    nc += 1
  if (x-1, y) in r and (x, y-1) in r and (x-1, y-1) not in r:
    nc += 1
  return nc

def numSides(r):
  ns = 0
  for p in r:
    nc = numCorners(p, r)
    ns += nc
  return ns

def solve2(lines):
  regions = getRegions(lines)
  price = 0
  for r in regions:
    for p in r:
      x, y = p
      pl = lines[y][x]
      break
    ns = numSides(r)
#    print(f"{pl}: {ns}")
    price += ns*len(r)
  print("Solution 2: ", price)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
