# Author: Peter Jensen

import sys
import re
class Config:
  title = "--- Day 03: Mull It Over ---"
  input = "input-03.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def solve1(lines):
  muls = []
  for l in lines:
    lr = l
    while len(lr) > 0:
      m = re.search(r"mul\(\d{1,3},\d{1,3}\)", lr)
      if m == None:
        break
      else:
        muls.append(m.group(0))
        lr = lr[m.end():]
  sum = 0
  for mul in muls:
    m = re.search(r"(\d+),(\d+)", mul)
    sum += int(m.group(1)) * int(m.group(2))
  print("Solution 1: ", sum)

def solve2(lines):
  insts = []
  for l in lines:
    lr = l
    while len(lr) > 0:
      m = re.search(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", lr)
      if m == None:
        break
      else:
        insts.append(m.group(0))
        lr = lr[m.end():]
  sum = 0
  useMul = True
  for inst in insts:
    m = re.search(r"(\d+),(\d+)|do\(\)|don't\(\)", inst)
    if m.group(0) == "do()":
      useMul = True
    elif m.group(0) == "don't()":
      useMul = False
    else:
      if useMul:
        sum += int(m.group(1)) * int(m.group(2))
  print("Solution 2: ", sum)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
