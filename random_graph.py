import random
import sys
import time

size = sys.argv[1]
size = int(size)
clique_size = 4
#clique_size = sys.argv[2]
#clique_size = int(clique_size)

filename = sys.argv[2]
f = open(filename, 'w')


nodes = {}
adj_list = {}
i = 0
while i<size:
	nodes[i] = False
	i += 1

random.seed(time.time())

def allTrue():
	i = 0
	while i < size:
		if nodes[i] == False:
			return False
		i += 1
	return True

numOfEdges = 0

allNodesTrue = False
while allNodesTrue == False:
	clique = {}
	while len(clique) < clique_size:
		num = len(clique)
		#print str(num) + " " + str(allNodesTrue)
		allNodesTrue = allTrue()
		if allNodesTrue == True:
			break
		rand = random.randint(1,size)
		while nodes[rand-1] == True:
			rand = random.randint(1,size)
		clique[num] = rand
		nodes[rand-1] = True
	#end while
	
	if len(clique) > 1:
		i = 0
		while i < len(clique):
			j = 0
			while j < len(clique):
				if j == i: #to avoid self-loops
					j += 1
					continue
				
				ran = random.random()
				if ran < 0.66:
					if ran < 0.46:
						f.write(str(clique[i]) + " " + str(clique[j])+ " 1 0\n")
					else:
						f.write(str(clique[i]) + " " + str(clique[j])+ " 0 1\n")
					if clique[i] in adj_list:
						adj_list[ clique[i] ].append(clique[j])
					else:
						adj_list[ clique[i] ] = []
						adj_list[ clique[i] ].append(clique[j])
					numOfEdges += 1
				#end if
				j += 1
			#end while
			i += 1
		#end while
	#allNodesTrue = allTrue()

print "Number of edges used in clique: " + str(numOfEdges)


i = 1
while i <= size:
	rand1 = random.randint(1,size)
	rand2 = random.randint(1,size)
	while ( (rand1 in adj_list) and (rand2 in adj_list[rand1]) ) or rand1 == rand2:
		rand1 = random.randint(1,size)
		rand2 = random.randint(1,size)
	
	ran = random.random()
	#print ran
	if ran < 0.66:
		if ran < 0.46:
			f.write(str(rand1) + " " + str(rand2)+ " 1 0\n")
		else:
			f.write(str(rand1) + " " + str(rand2)+ " 0 1\n")
		if rand1 in adj_list:
			adj_list[rand1].append(rand2)
		else:
			adj_list[rand1] = []
			adj_list[rand1].append(rand2)
		numOfEdges += 1
	#end if
	i += 1

print "Total number of edges: " + str(numOfEdges)


f.close()
