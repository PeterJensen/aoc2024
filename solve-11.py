# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 11: Plutonian Pebbles ---"
  input = "input-11.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def stoneCount(num, blinks):
  if blinks == 0:
    return 1
  if num == 0:
    return stoneCount(1, blinks - 1)
  elif len(str(num)) % 2 == 0:
    sn = str(num)
    l = len(sn) // 2
    n1, n2 = int(sn[0:l]), int(sn[l:])
    return stoneCount(n1, blinks - 1) + stoneCount(n2, blinks - 1)
  else:
    return stoneCount(num*2024, blinks - 1)

def stoneCountWithCache(num, blinks, cache):
  k = (num, blinks)
  if k in cache.keys():
    return cache[k]
  if blinks == 0:
    return 1
  if num == 0:
    c = stoneCountWithCache(1, blinks - 1, cache)
    cache[(num, blinks)] = c
    return c
  elif len(str(num)) % 2 == 0:
    sn = str(num)
    l = len(sn) // 2
    n1, n2 = int(sn[0:l]), int(sn[l:])
    c = stoneCountWithCache(n1, blinks - 1, cache) + stoneCountWithCache(n2, blinks - 1, cache)
    cache[(num, blinks)] = c
    return c
  else:
    c = stoneCountWithCache(num*2024, blinks - 1, cache)
    cache[(num, blinks)] = c
    return c

def solve1(lines):
  c = 0
  for n in lines[0].split(" "):
    c += stoneCount(int(n), 25)
  print("Solution 1: ", c)

def solve2(lines):
  c = 0
  for n in lines[0].split(" "):
    c += stoneCountWithCache(int(n), 75, {})
  print("Solution 2: ", c)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
