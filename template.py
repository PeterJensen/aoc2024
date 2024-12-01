# Author: Peter Jensen

import sys

class Config:
  title = "--- Day xx:  ---"
  input = "input-xx.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def solve1(lines):
  print("Solution 1: ")

def solve2(lines):
  print("Solution 2: ")
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
