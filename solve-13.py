# Author: Peter Jensen

import sys
import re

class Config:
  title = "--- Day 13: Claw Contraption ---"
  input = "input-13.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Machine:
  def __init__(self, lines):
    self.buttonA = [int(n) for n in re.findall(r"\+(\d+)", lines[0])]
    self.buttonB = [int(n) for n in re.findall(r"\+(\d+)", lines[1])]
    self.prize = [int(n) for n in re.findall(r"=(\d+)", lines[2])]
  def __repr__(self):
    return f"A: {self.buttonA}, B: {self.buttonB}, Prize: {self.prize}"
  def solutions(self):
    solutions = []
    ax, ay = self.buttonA
    bx, by = self.buttonB
    px, py = self.prize
    for a in range(101):
      b = (px - a*ax) // bx
      if a*ax + b*bx != px or a*ay + b*by != py:
        continue
      solutions.append((a, b))
    return solutions
  def bestSolution(self):
    bs = None
    bc = None
    sols = self.solutions()
    for s in sols:
      a, b = s
      c = 3*a + b
      if bs == None or c < bc:
        bc = c
        bs = s
    return bs, bc
  def computedSolution(self):
    ax, ay = self.buttonA
    bx, by = self.buttonB
    px, py = self.prize
    a = (bx*py - by*px) / (ay*bx - ax*by)
    b = (px - a*ax) / bx
    if a == int(a) and b == int(b):
      return (int(a), int(b)), int(3*a+b)
    else:
      return None, None

def solve1(lines):
  totalCost = 0
  for ml in range(0, len(lines), 4):
    m = Machine(lines[ml:ml+3])
    solution, cost = m.bestSolution()
    if solution != None:
      totalCost += cost
  print("Solution 1: ", totalCost)

def solve2(lines):
  totalCost = 0
  for ml in range(0, len(lines), 4):
    m = Machine(lines[ml:ml+3])
    m.prize = [m.prize[0] + 10000000000000, m.prize[1] + 10000000000000]
    solution, cost = m.computedSolution()
    if solution != None:
      totalCost += cost
  print("Solution 2: ", totalCost)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
