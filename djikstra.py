# Author: Peter Jensen

from collections import defaultdict 

class QueueElem:
  def __init__(self, node, prio):
    self.node = node
    self.prio = prio
  def __repr__(self):
    return f"{self.node}: {self.prio}"

class Queue:
  def __init__(self):
    self.queue = []
    self.elems = set()
  def addWithPriority(self, elem):
    self.elems.add(elem.node)
    if len(self.queue) == 0:
      self.queue.append(elem)
      return
    for ei, e in enumerate(self.queue):
      if e.prio <= elem.prio:
        self.queue.insert(ei, elem)
        #if ei != 0:
        #  print(f"addWithPriority: {ei}")
        return
    self.queue.append(elem)
  def extractMin(self):
    elem = self.queue.pop()
    self.elems.remove(elem.node)
    return elem
  def isEmpty(self):
    return len(self.queue) == 0
  def isInQueue(self, node):
    return node in self.elems
  def decreasePriority(self, node, prio):
    for e in self.queue:
      if e.node == node:
        e.prio = prio
        break
    self.queue.sort(key = lambda e: e.prio, reverse = True)
  def __repr__(self):
    return f"{self.queue}"

def shortest(start, end):
  dist = defaultdict(lambda: 999999999)
  prev = defaultdict(lambda: None)
  dist[start] = 0
  queue = Queue()
  queue.addWithPriority(QueueElem(start, dist[start]))
  qLen = 1000
  hasDistTo = hasattr(start, "distTo") and callable(start.distTo)
  def distBetween(s, d):
    if hasDistTo:
      return s.distTo(d)
    else:
      return 1
  while not queue.isEmpty():
#    print(f"queue: {queue}")
    if len(queue.queue) > qLen:
#      print(f"Queue Length: {len(queue.queue)}")
      #queue.print()
      qLen += 1000
#      print("Minimum Elem:")
#      queue.queue[-1].print()
    u = queue.extractMin()
#    print(f"queue.extractMin: {u}")
    if u.node.match(end):
      return dist, prev
    numNeighbors = 0
    for v in u.node.neighbors():
      numNeighbors += 1
      alt = dist[u.node] + distBetween(u.node, v)
      if alt < dist[v]:
        dist[v] = alt
        prev[v] = u.node
        if queue.isInQueue(v):
          queue.decreasePriority(v, alt)
        else:
          queue.addWithPriority(QueueElem(v, alt))
    if numNeighbors == 0:
      None
      #print(f"No moves for: {u.node}")
  return dist, prev

def allShortest(start, end):
  dist = defaultdict(lambda: 999999999)
  prev = defaultdict(lambda: set())
  dist[start] = 0
  queue = Queue()
  queue.addWithPriority(QueueElem(start, dist[start]))
  qLen = 1000
  hasDistTo = hasattr(start, "distTo") and callable(start.distTo)
  def distBetween(s, d):
    if hasDistTo:
      return s.distTo(d)
    else:
      return 1
  while not queue.isEmpty():
#    print(f"queue: {queue}")
    if len(queue.queue) > qLen:
#      print(f"Queue Length: {len(queue.queue)}")
      #queue.print()
      qLen += 1000
#      print("Minimum Elem:")
#      queue.queue[-1].print()
    u = queue.extractMin()
#    print(f"queue.extractMin: {u}")
    if u.node.match(end):
      return dist, prev
    numNeighbors = 0
    for v in u.node.neighbors():
      numNeighbors += 1
      alt = dist[u.node] + distBetween(u.node, v)
      if alt <= dist[v]:
        dist[v] = alt
        prev[v].add(u.node)
        if queue.isInQueue(v):
          queue.decreasePriority(v, alt)
        else:
          queue.addWithPriority(QueueElem(v, alt))
    if numNeighbors == 0:
      None
      #print(f"No moves for: {u.node}")
  return dist, prev

def longest(start, end):
  dist = defaultdict(lambda: 0)
  prev = defaultdict(lambda: None)
  dist[start] = 0
  queue = Queue()
  queue.addWithPriority(QueueElem(start, dist[start]))
  qLen = 10
  while not queue.isEmpty():
    #if len(queue.queue) > qLen:
    #  print(f"Queue Length: {len(queue.queue)}")
    #  queue.print()
    #  qLen += 10
    #  print("Minimum Elem:")
    #  queue.queue[-1].print()
    u = queue.extractMin()
    if u.node.match(end):
      continue
    numNeighbors = 0
    for v in u.node.neighbors():
      numNeighbors += 1
      alt = dist[u.node] - 1
      if alt < dist[v]:
        dist[v] = alt
        prev[v] = u.node
        if queue.isInQueue(v):
          queue.decreasePriority(v, alt)
        else:
          queue.addWithPriority(QueueElem(v, alt))
    if numNeighbors == 0:
      None
      #print(f"No moves for: {u.node}")
  return dist, prev
