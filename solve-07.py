# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 07: Bridge Repair ---"
  input = "input-07.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]


def solve1(lines):
  sum = 0
  for l in lines:
    val, nums = l.split(": ")
    val = int(val)
    nums = [int(n) for n in nums.split(" ")]
    nops = len(nums) - 1
    for pops in itertools.product("+*", repeat = nops):
      v = nums[0]
      for opi, op in enumerate(pops):
        if op == "+":
          v += nums[opi+1]
        elif op == "*":
          v *= nums[opi+1]
        if v >= val:
          break
      if v == val:
        sum += val
        break
  print("Solution 1: ", sum)

def solve2(lines):
  sum = 0
  for l in lines:
    val, nums = l.split(": ")
    val = int(val)
    nums = [int(n) for n in nums.split(" ")]
    nops = len(nums) - 1
    for pops in itertools.product(["+", "*", "||"], repeat = nops):
      v = nums[0]
      for opi, op in enumerate(pops):
        if op == "+":
          v += nums[opi+1]
        elif op == "*":
          v *= nums[opi+1]
        elif op == "||":
          v = int(str(v) + str(nums[opi+1]))
        if v > val:
          break
      if v == val:
        sum += val
        break
  print("Solution 2: ", sum)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
