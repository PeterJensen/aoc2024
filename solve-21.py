# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 21: Keypad Conundrum ---"
  input = "input-21.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Reverse:
  rev = {">": "<", "<": ">", "^": "v", "v": "^"}
  @classmethod
  def make(cls, seq):
    return "".join([cls.rev[m] for m in reversed(seq)])

class NumMoves:
  shortest = {
    "A0": ("<",),
    "A1": ("<^<", "^<<"),
    "A2": ("<^", "^<"),
    "A3": ("^", ),
    "A4": ("<^<^", "<^^<", "^<<^", "^<^<", "^^<<"),
    "A5": ("<^^", "^^<", "^<^"),
    "A6": ("^^",),
    "A8": ("<^^^", "^<^^", "^^<^", "^^^<"),
    "A9": ("^^^",),
    "02": ("^",),
    "05": ("^^",),
    "08": ("^^^",),
    "14": ("^",),
    "17": ("^^",),
    "18": ("^^>", ">^^", "^>^"),
    "29": ("^^>", "^>^", ">^^"),
    "36": ("^",),
    "37": ("<<^^", "<^<^", "<^^<", "^<<^", "^<^<", "^^<<"),
    "38": ("<^^", "^^<", "^<^"),
    "40": ("v>v", ">vv"),
    "45": (">",),
    "56": (">",),
    "6A": ("vv",),
    "76": (">>v", "v>>", ">v>"),
    "79": (">>",),
    "80": ("vvv",),
    "98": ("<",),
    "9A": ("vvv", )}

class DirMoves:
  shortest = {
    "A^": ("<",),
    "A>": ("v",),
#    "Av": ("<v", "v<"), # <vA:1+2, v<A:1+3 
    "Av": ("<v",),
#    "A<": ("<v<", "v<<"), # <v<A:1+1+3, v<<A:1+0+3
    "A<": ("v<<",),
#    "Av": ("<v", "v<"), # <vA:1+2, v<A:1+3
    "Av": ("<v",),
    "^v": ("v",),
    "^<": ("v<",),
    "^>": ("v>",),
    "v<": ("<",),
    "v>": (">",),
    "<>": (">>",)
  }

class Keypad:
  def __init__(self, shortest):
    self.shortest = shortest
    self.cache = {}
  def shortestToKey(self, fromKey, toKey):
    if fromKey == toKey:
      yield "A"
      return
    ftk = fromKey + toKey
    if ftk in self.shortest.keys():
      for seq in self.shortest[ftk]:
        yield seq + "A"
      return
    tfk = toKey + fromKey
    if tfk in self.shortest.keys():
      seqs = [Reverse.make(seq) for seq in self.shortest[tfk]]
      self.shortest[ftk] = seqs
      for seq in seqs:
        yield seq + "A"
  def shortestSeqs(self, keys):
    keys = "A" + keys
    its = []
    for pi in range(len(keys)-1):
      its.append(self.shortestToKey(keys[pi], keys[pi+1]))
    for seq in itertools.product(*its, repeat = 1):
      yield "".join(seq)
  def bestToKey(self, fromKey, toKey):
    if fromKey == toKey:
      return "A"
    ftk = fromKey + toKey
    if ftk in self.shortest.keys():
      return self.shortest[ftk][0] + "A"
    tfk = toKey + fromKey
    if tfk in self.shortest.keys():
      rs = Reverse.make(tfk)
      self.shortest[ftk] = (rs, )
      return rs + "A"
    print("ERROR")
  def bestSeq(self, keys):
    seq = ""
    for pi in range(len(keys)-1):
      seq += self.bestToKey(keys[pi], keys[pi+1])
    return seq
  def bestSeqLen(self, keys, numRobots):
    ck = (keys, numRobots)
    if ck in self.cache:
      return self.cache[ck]
    if numRobots == 0:
      return len(keys)-1
    bs = "A" + self.bestSeq(keys)
    l = 0
    for pi in range(0,len(bs)-1):
      l += self.bestSeqLen(bs[pi:pi+2], numRobots-1)
    self.cache[ck] = l
    return l

def shortestSeq(nums):
  nkp = Keypad(NumMoves.shortest)
  dkp = Keypad(DirMoves.shortest)
  ss  = None
  for s1 in nkp.shortestSeqs(nums):
    for s2 in dkp.shortestSeqs(s1):
      for s3 in dkp.shortestSeqs(s2):
        if ss == None or len(s3) < len(ss):
          ss = s3
  return ss

def shortestSeqLen(nums):
  nkp = Keypad(NumMoves.shortest)
  dkp = Keypad(DirMoves.shortest)
  sl = None
  for s1 in nkp.shortestSeqs(nums):
    l = dkp.bestSeqLen("A" + s1, 25)
    if sl == None or l < sl:
      sl = l
  return sl

def solve1(lines):
  sum = 0
#  for l in ["029A", "980A", "179A", "456A", "379A"]:
  for l in lines:
    ss = shortestSeq(l)
#    print(f"{l} {len(ss)} {ss}")
    sum += int(l[0:-1]) * len(ss)
  print("Solution 1: ", sum)

def solve2(lines):
  sum = 0
#  for l in ["029A", "980A", "179A", "456A", "379A"]:
  for l in lines:
    sl = shortestSeqLen(l)
#    print(f"{l} {sl}")
    sum += int(l[0:-1]) * sl
  print("Solution 2: ", sum)
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
