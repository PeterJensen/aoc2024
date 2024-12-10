# Author: Peter Jensen

import sys

class Config:
  title = "--- Day 09: Disk Fragmenter ---"
  input = "input-09.txt"

def getLines():
  file = Config.input if len(sys.argv) < 2 else sys.argv[1]
  return None if file == "" else [l.strip() for l in open(file, 'r').readlines()]

def getDisk(line):
  disk = []
  freeBlock = False
  fileId = 0
  for nb in line:
    nb = int(nb)
    if freeBlock:
      disk += [-1]*nb
    else:
      disk += [fileId]*nb
      fileId += 1
    freeBlock = not freeBlock
  return disk

def compact(disk):
  def nextMove(i):
    nm = i - 1
    while nm >= 0 and disk[nm] == -1:
      nm -= 1
    return nm
  def swap(i, j):
    t = disk[i]
    disk[i] = disk[j]
    disk[j] = t
  nextFree = disk.index(-1)
  moveFrom = nextMove(len(disk))
  while moveFrom != -1 and moveFrom > nextFree:
    swap(nextFree, moveFrom)
    nextFree = disk.index(-1, nextFree + 1)
    moveFrom = nextMove(moveFrom)
  
def checksum(disk):
  c = 0
  for i,e in enumerate(disk):
    if e != -1:
      c += i*e
  return c

def solve1(lines):
  disk = getDisk(lines[0])
  compact(disk)
  print("Solution 1: ", checksum(disk))

def getDisk2(line):
  fileBlocks = []
  freeBlocks = []
  fileId = 0
  freeBlock = False
  blockIndex = 0
  for nb in line:
    nb = int(nb)
    if freeBlock:
      if nb > 0:
        freeBlocks.append((blockIndex, nb))
    else:
      if nb > 0:
        fileBlocks.append((fileId, blockIndex, nb))
      fileId += 1
    blockIndex += nb
    freeBlock = not freeBlock
  return fileBlocks, freeBlocks

def defrag(fileBlocks, freeBlocks):
  def findFreeBlock(size, maxPos):
    for freeIndex, (freePos, freeSize) in enumerate(freeBlocks):
      if freeSize >= size and freePos < maxPos:
        return freeIndex
    return -1
  def combineFree():
    freeBlocks.sort(key = lambda v: v[0])
    fi = 0
    while fi < len(freeBlocks)-1:
      p, s = freeBlocks[fi]
      np, ns = freeBlocks[fi+1]
      if p+s == np:
        freeBlocks[fi] = (p, s+ns)
        freeBlocks.pop(fi+1)
      else:
        fi += 1
#  def insertFree(pos, size):
#    for fi, (fp, fs) in enumerate(freeBlocks):
#      if fp > pos:
#        freeBlocks.insert(fi, (pos, size))
#        return
#    freeBlocks.append((pos, size))
  for fileIndex in range(len(fileBlocks)-1, -1, -1):
    fileId, filePos, fileSize = fileBlocks[fileIndex]
    freeIndex = findFreeBlock(fileSize, filePos)
    freePos, freeSize = freeBlocks[freeIndex]
    if freeIndex != -1:
#      insertFree(filePos, fileSize)
      freeBlocks.append((filePos, fileSize))
      fileBlocks[fileIndex] = (fileId, freePos, fileSize)
      if fileSize == freeSize:
        freeBlocks.pop(freeIndex)
      else:
        freeBlocks[freeIndex] = (freePos + fileSize, freeSize - fileSize)
      combineFree()

def checksum2(fileBlocks):
  c = 0
  for (id, pos, size) in fileBlocks:
    for pi in range(pos, pos+size):
      c += pi * id
  return c

def solve2(lines):
  fileBlocks, freeBlocks = getDisk2(lines[0])
  defrag(fileBlocks, freeBlocks)
  print("Solution 2: ", checksum2(fileBlocks))
  
def main():
  print(Config.title)
  lines = getLines()
  solve1(lines)
  solve2(lines)

if __name__ == "__main__":
  main()
