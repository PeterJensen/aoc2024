# Author: Peter Jensen

import sys
import itertools

class Config:
  title = "--- Day 24: Crossed Wires ---"
  input = "input-24.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def parse(lines):
  inits = {}
  connections = []
  for l in lines:
    if l == "":
      continue
    if l.find(":") != -1:
      w, v = l.split(": ")
      inits[w] = int(v)
    else:
      gate, out = l.split(" -> ")
      l, o, r = gate.split(" ")
      connections.append((l, o, r, out))
  return inits, connections

def evaluate(inits, outputs):
  values = {k:v for k,v in inits.items()}
  keepGoing = True
  while keepGoing:
    keepGoing = False
    for o, (l, op, r) in outputs.items():
      if l in values.keys() and r in values.keys():
        if o in values.keys():
          continue
        lv, rv = values[l], values[r]
        if op == "AND":
          values[o] = lv & rv
        elif op == "OR":
          values[o] = lv | rv
        elif op == "XOR":
          values[o] = lv ^ rv
        keepGoing = True
  xs = ""
  ys = ""
  zs = ""
  for iv in sorted(values.keys(), reverse = True):
    if iv[0] == 'x':
      xs += str(values[iv])
    elif iv[0] == 'y':
      ys += str(values[iv])
    elif iv[0] == 'z':
      zs += str(values[iv])
  return xs, ys, zs

def solve1(lines):
  inits, connections = parse(lines)
  outputs = {c[3]:c[0:3] for c in connections}
  xs, ys, zs = evaluate(inits, outputs)
#  print(f" {xs}")
#  print(f" {ys}")
#  print(f"{zs}")
  zi = int(zs, 2)
#  print(bin(int(xs, 2) + int(ys, 2))[2:])
  marks = "".join(reversed([str(n)[-1] for n in range(46)]))
#  print(marks)
  print("Solution 1: ", int(zs, 2))

def expand(o, outputs):
  l, op, r = outputs[o]
  if l[0] != 'x' and l[0] != 'y':
    l = expand(l, outputs)
  if r[0] != 'x' and r[0] != 'y':
    r = expand(r, outputs)
  if len(l) > 3:
    l = f"({l})"
  if len(r) > 3:
    r = f"({r})"
  if len(l) == 3 and len(r) == 3:
#    print(f"Checking: {l} {op} {r}")
    if l[1:] != r[1:] or (l[0] == r[0]):
      print(f"ERROR: {l} {op} {r}") 
  return f"{l} {op} {r}"

def swap(a, b, outputs):
  t = outputs[a]
  outputs[a] = outputs[b]
  outputs[b] = t

def makeOutputs(nBits):
  outputs = {}
  for i in range(1,nBits):
    outputs[f"e{i:02}"] = (f"x{i:02}", "XOR", f"y{i:02}")
  for i in range(0,nBits):
    outputs[f"a{i:02}"] = (f"x{i:02}", "AND", f"y{i:02}")
  c = "a00"
  for i in range(2, nBits):
    outputs[f"i{i:02}"] = (c, "AND", f"e{i-1:02}")
    outputs[f"c{i:02}"] = (f"a{i-1:02}", "OR", f"i{i:02}")
    c = f"c{i:02}"
  outputs["z00"] = ("x00", "XOR", "y00")
  outputs["z01"] = ("a00", "XOR", "e01")
  for i in range(2, nBits):
    outputs[f"z{i:02}"] = (f"c{i:02}", "XOR", f"e{i:02}")
  outputs[f"i{nBits:02}"] = (c, "AND", f"e{nBits-1:02}")
  outputs[f"z{nBits:02}"] = (f"a{nBits-1:02}", "OR", f"i{nBits:02}")
  return outputs

def rank(o, outputs):
  if o[0] == "x":
    return int(o[1:])
  elif o[0] == "y":
    return 100 + int(o[1:])
  else:
    l, op, r = outputs[o]
    return min(rank(l, outputs), rank(r, outputs))

def normalize(outputs):
  normOutputs = {}
  for k,v in outputs.items():
    l, op, r = v
    if rank(l, outputs) > rank(r, outputs):
      normOutputs[k] = (r, op, l)
    else:
      normOutputs[k] = v
  return normOutputs

def findGood(good, outputs):
  for k,v in outputs.items():
    if expand(k, outputs) == good:
      return k
  return None

def solve2(lines):
  inits, connections = parse(lines)
  outputs = normalize({c[3]:c[0:3] for c in connections})
  goodOutputs = normalize(makeOutputs(45))
  # find z swaps
  lastFail = None
  swaps = []
  for z in range(45):
    outZ = f"z{z:02}"
    check = expand(outZ, outputs)
    good  = expand(outZ, goodOutputs)
    if check != good:
      lastFail = outZ
      goodSwap = findGood(good, outputs)
      if goodSwap != None:
        swaps += [outZ, goodSwap]
        swap(outZ, goodSwap, outputs)
      else:
        break
  if lastFail != None:
    lf, op, rf = outputs[lastFail]
    lg, op, rg = goodOutputs[lastFail]
    lfe = expand(lf, outputs)
    lge = expand(lg, goodOutputs)
    rfe = expand(rf, outputs)
    rge = expand(rg, goodOutputs)
    if lfe != lge:
      goodSwap = findGood(lge, outputs)
      if goodSwap != None:
        swaps += [lf, goodSwap]
    elif rfe != rge:
      goodSwap = findGood(rge, outputs)
      if goodSwap != None:
        swaps += [rf, goodSwap]

  print("Solution 2:", ",".join(sorted(swaps)))

def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
