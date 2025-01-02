# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 23: LAN Party ---"
  input = "input-23.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def getNetwork(lines):
  network = {}
  for l in lines:
    a, b = l.split("-")
    network[a] = network.get(a, set())
    network[b] = network.get(b, set())
    network[a].add(b)
    network[b].add(a)
  return network

def findTriplets(network):
  triplets = set()
  for a,b in itertools.combinations(network.keys(), r = 2):
    if a in network[b]:
      for c in network[a] & network[b]:
        t = tuple(sorted([a,b,c]))
        if t not in triplets:
          triplets.add(t)
  return triplets

def canAdd(lan, node, network):
  for n in lan:
    if node not in network[n]:
      return False 
  return True

def getInitLans(network):
  lans = set()
  for a, v in network.items():
    for b in v:
      lans.add(tuple(sorted([a, b]))) 
  return lans

def expandLans(lans, network):
  newLans = set()
  for lan in lans:
    for n in network.keys():
      if canAdd(lan, n, network):
        newLans.add(tuple(sorted(list(lan) + [n])))
  return newLans

def solve1(lines):
  network = getNetwork(lines)
  triplets = findTriplets(network)
  sum = 0
  for t in triplets:
    hasTs = [c for c in t if c[0] == "t"]
    if len(hasTs) > 0:
      sum += 1
  print("Solution 1: ", sum)

def solve2(lines):
  network = getNetwork(lines)
  lans = getInitLans(network)
  while True:
    nextLans = expandLans(lans, network)
    if len(nextLans) == 0:
      break
    lans = nextLans
  print("Solution 2: ", ",".join(list(lans)[0]))
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
