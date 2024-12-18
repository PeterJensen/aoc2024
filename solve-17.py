# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 17: Chronospatial Computer ---"
  input = "input-17.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

class Computer:
  instNames = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
  def __init__(self, lines):
    self.regs = dict()
    for ri, r in enumerate("ABC"):
      self.regs[r] = int(lines[ri].split()[2])
    self.programStr = lines[4].split()[1]
    self.program = tuple(map(int, self.programStr.split(",")))
    self.pc = 0
    self.output = ""
    self.doTrace = False
  def __repr__(self):
    return f"Registers: {self.regs}\nProgram: {self.program}"
  
  def printProgram(self):
    for pc in range(0, len(self.program), 2):
      print(f"{pc}: {self.instNames[self.program[pc]]} {self.program[pc+1]}")

  def comboValue(self, op):
    if op <= 3:
      return op
    else:
      return self.regs["ABC"[op-4]]

  def trace(self):
    if self.doTrace:
      inst, op = self.program[self.pc:self.pc+2]
      print(f"{self.pc}: {self.instNames[inst]} {op} Regs:{self.regs}")

  def step(self):
    if self.pc >= len(self.program):
      return False
    inst, op = self.program[self.pc:self.pc+2]
    self.trace();
    match inst:
      case 0: # adv
        self.regs["A"] = self.regs["A"] >> self.comboValue(op)
      case 1: # bxl
        self.regs["B"] = self.regs["B"] ^ op
      case 2: # bst
        self.regs["B"] = self.comboValue(op) & 7
      case 3: # jnz
        if self.regs["A"] != 0:
          self.pc = op - 2
      case 4: # bxc
        self.regs["B"] = self.regs["B"] ^ self.regs["C"]
      case 5: # out
        if self.output != "":
          self.output += ","
        self.output += str(self.comboValue(op) & 7)
      case 6: # bdv
        self.regs["B"] = (self.regs["A"] >> self.comboValue(op))
      case 7: # cdv
        self.regs["C"] = (self.regs["A"] >> self.comboValue(op))
    self.pc += 2
    return True

  def run(self):
    doRun = True
    while doRun:
      doRun = self.step()

  def reset(self):
    self.pc = 0
    for r in "ABC":
      self.regs[r] = 0
    self.output = ""

def runPgm(aStart):
  a = aStart
  output = ""
  while a > 0:
    b = (a & 7) ^ 1
    c =  (a >> b) & 7  # & 7 because only last 3 bits matter
    b = b ^ c ^ 6
    a = a >> 3
    if output != "":
      output += ","
    output += str(b)
  return output

def solve1(lines):
  computer = Computer(lines)
  computer.run()
  print("Solution 1: ", computer.output)

def getValidAs(digit, expected, validAs):
  newValidAs = []
  if digit == 0:
    for a in range(1024):
      output = runPgm(a)
      if output[2*digit:2*digit+1] == expected[2*digit:2*digit+1]:
        newValidAs.append(a)
  else:
    for a in range(8):
      upperA = a << (7 + 3*digit)
      for av in validAs:
        newA = upperA + av
        output = runPgm(newA)
        if output[2*digit:2*digit+1] == expected[2*digit:2*digit+1]:
          newValidAs.append(newA)
  return newValidAs

def solve2(lines):
  expected = "2,4,1,1,7,5,0,3,4,7,1,6,5,5,3,0"
  validAs = []
  for d in range(len(expected)//2 + 1):
    validAs = getValidAs(d, expected, validAs)
#    print(f"digit: {d}, expected: {expected[d*2:d*2+1]}")
#  for a in validAs:
#    print(f"{a:o}: {runPgm(a)}")
  print("Solution 2: ", validAs[0])
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
