# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 02: Red-Nosed Reports ---"
  input = "input-02.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def isSafe(nums):
  if nums[0] < nums[1]:
    for ni, n in enumerate(nums):
      if ni > 0:
        if n <= nums[ni-1] or n - nums[ni-1] > 3:
          return False
    return True
  if nums[0] > nums[1]:
    for ni, n in enumerate(nums):
      if ni > 0:
        if n >= nums[ni-1] or nums[ni-1] - n > 3:
          return False
    return True
  return False

def solve1(lines):
  ns = 0
  for l in lines:
    nums = [int(n) for n in l.split(" ")]
    if isSafe(nums):
      ns += 1
  print("Solution 1: ", ns)

def solve2(lines):
  ns = 0
  for l in lines:
    nums = [int(n) for n in l.split(" ")]
    for i in range(len(nums)):
      n = nums.pop(i)
      if isSafe(nums):
        ns += 1
        break
      nums.insert(i, n)
  print("Solution 2: ", ns)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
