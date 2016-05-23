from LRU import alg


lru = alg(5)

lru.walk()
print('Loop starting')
for i in range(5):
    assert lru.get(i) == None
    lru.put(i, i*i)
    assert lru.get(i) == i*i
    assert lru.head.key == i
    lru.walk()
    dist, found  =  lru.get_stackdistance(0)

    print(dist,found)
    assert dist == i
assert lru.tail.key == 0

assert lru.get(0) == 0
lru.walk()
assert lru.tail.key == 1

dist, found  =  lru.get_stackdistance(0)
print(dist,found)
assert dist == 0

lru.print_statistics()


