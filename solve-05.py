# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 05: Print Queue ---"
  input = "input-05.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def parse(lines):
  orders = set()
  nums = []
  doOrders = True  
  for l in lines:
    if l == "":
      doOrders = False
      continue
    if doOrders:
      orders.add(tuple([int(i) for i in l.split("|")]))
    else:
      nums.append(tuple([int(i) for i in l.split(",")]))
  return orders, nums

def isCorrect(seq, orders):
  for e1, e2 in itertools.combinations(seq, 2):
    if (e2, e1) in orders:
      return False
  return True

def solve1(lines):
  orders, nums = parse(lines)
  sum = 0
  for seq in nums:
    if isCorrect(seq, orders):
      sum += seq[len(seq) // 2]
  print("Solution 1: ", sum)

def reorder(seq, orders):
  oldSeq = list(seq)
  if len(oldSeq) == 0:
    return []
  for e1 in oldSeq:
    isOk = True
    for e2 in oldSeq:
      if e1 != e2:
        if (e2, e1) in orders:
          isOk = False
    if isOk:
      oldSeq.remove(e1)
      return [e1] + reorder(oldSeq, orders)

def solve2(lines):
  orders, nums = parse(lines)
  sum = 0
  for seq in nums:
    if not isCorrect(seq, orders):
      newSeq = reorder(seq, orders)
      sum += newSeq[len(newSeq) // 2]
  print("Solution 2: ", sum)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
