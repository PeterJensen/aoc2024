# Author: Peter Jensen

import sys
import re

class Config:
  title = "--- Day 14: Restroom Redoubt ---"
  input = "input-14.txt"
  gridSize = (101, 103)

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Robot:
  def __init__(self, size, line):
    numbers = re.findall(r"[+-]?\d+", line)
    px, py, vx, vy = list(map(int, numbers))
    self.p = (px, py)
    self.v = (vx, vy)
    self.size = size
  def __repr__(self):
    return f"p={self.p} v={self.v}"
  def move(self, secs=1):
    px, py = self.p
    vx, vy = self.v
    sx, sy = self.size
    self.p = ((px + secs*vx) % sx, (py + secs*vy) % sy)
  def quadrantOf(self):
    qx, qy = self.size[0] // 2, self.size[1] // 2
    px, py = self.p
    if px < qx and py < qy:
      return 0
    elif px > qx and py < qy:
      return 1
    elif px > qx and py > qy:
      return 2
    elif px < qx and py > qy:
      return 3
    return None

def getRobots(lines):
  return [Robot(Config.gridSize, l) for l in lines]  

def solve1(lines):
  robots = getRobots(lines)
  for r in robots:
    r.move(100)
  quadrants = [0 for _ in range(4)]
  for r in robots:
    q = r.quadrantOf()
    if q != None:
      quadrants[q] += 1
  safety = 1
  for q in quadrants:
    safety *= q
  print("Solution 1: ", safety)

def robotImage(robots):
  gx, gy = Config.gridSize
  robotPos = [r.p for r in robots]
  s = ""
  for y in range(gy):
    l = "".join(["." if robotPos.count((x, y)) == 0 else "x" for x in range(gx)])
    s += l + "\n"
  return s

def solve2(lines):
  robots = getRobots(lines)
  for r in robots:
    r.move(6000)
  for i in range(6001, 30001):
    if i % 10 == 0:
      print(i)
    for r in robots:
      r.move()
    ri = robotImage(robots)
    if ri.find("xxxxxxxxx") != -1:
      print(f"After {i}\n{ri}")
      break
  print("Solution 2: ")
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
