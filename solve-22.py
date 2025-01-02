# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 22: Monkey Market ---"
  input = "input-22.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def nextNumber(n):
  s1 = ((n*64) ^ n) % 16777216
  s2 = ((s1 >> 5) ^ s1) % 16777216
  s3 = ((s2*2048) ^ s2) % 16777216
  return s3

def next2000(n):
  for _ in range(2000):
    n = nextNumber(n)
  return n

def lastDigit(n):
  return int(str(n)[-1])

def all2000(n):
  all = [(lastDigit(n), None)]
  for i in range(1, 2001):
#  for i in range(1, 11):
    n = nextNumber(n)
    ld = lastDigit(n)
    all.append((ld, ld - all[i-1][0]))
  return all

def allSeqs(n):
  nums = all2000(n)
  seqs = {}
  for i in range(1, len(nums)- 4):
    seq = tuple([d[1] for d in nums[i:i+4]])
    if seq not in seqs:
      seqs[seq] = nums[i+3][0]
  return seqs

def solve1(lines):
  sum = 0
  for l in lines:
    sum += next2000(int(l))
  print("Solution 1: ", sum)

def solve2(lines):
  all = {}
  for l in lines:
    s = allSeqs(int(l))
    for k,v in s.items():
      if k in all.keys():
        all[k] += v
      else:
        all[k] = v
  maxBananas = max(all.values())
  print("Solution 2: ", maxBananas)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
