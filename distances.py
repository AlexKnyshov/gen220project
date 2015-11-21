from Bio import SeqIO
filename = raw_input("enter the filename")
infile = open(filename, "r")
seqs = {}
for seq in SeqIO.parse(infile, "fasta"):
    seqs[seq.id] = str(seq.seq)
#pairwise
names =[]
for key in seqs.keys():
	names.append(key)
distlist = []
matrix = [[0 for x in range(len(names)-1)] for y in range(len(names)-1)] #just for visualization
row = 0
inter = 0
for num in range(len(names)-1):
	pair1 = []
	pair1 += seqs[names[num]]
	for p2 in range(num+1, len(names)):
		pair2 = []
		pair2 += seqs[names[p2]]
		counter = 0
		countert = 0
		counterindel = 0
		startpos = 0
		endpos = len(pair1)
		#forward trim
		for index in range(len(pair1)):
			if pair1[index] != "-" and pair2[index] != "-":
				startpos = index
				break
		#reverse trim
		for index in range(len(pair1)-1, -1, -1):
			if pair1[index] != "-" and pair2[index] != "-":
				endpos = index
				break
		#checking the differences
		for index in range(startpos, endpos+1):
			if pair1[index] == "A" and pair2[index] == "G":
				countert += 1
			elif pair1[index] == "G" and pair2[index] == "A":
				countert += 1
			elif pair1[index] == "A" and pair2[index] == "C":
				counter +=1
			elif pair1[index] == "A" and pair2[index] == "T":
				counter +=1
			elif pair1[index] == "T" and pair2[index] == "A":
				counter +=1
			elif pair1[index] == "T" and pair2[index] == "G":
				counter +=1
			elif pair1[index] == "C" and pair2[index] == "T":
				countert +=1
			elif pair1[index] == "T" and pair2[index] == "C":
				countert +=1
			elif pair1[index] == "C" and pair2[index] == "A":
				counter +=1
			elif pair1[index] == "C" and pair2[index] == "G":
				counter +=1
			elif pair1[index] == "G" and pair2[index] == "C":
				counter +=1
			elif pair1[index] == "G" and pair2[index] == "T":
				counter +=1
			elif pair1[index] == "-" and pair2[index] != "-":
				counterindel +=1
			elif pair2[index] == "-" and pair1[index] != "-":
				counterindel +=1
		#calculating the distance
		val = round((float(counter)/(endpos-startpos)*100), 2)
		matrix[inter][row] = val
		distlist.append(val)
		inter += 1
	row +=1
	inter = 0
print "distance matrix (per cent)"
for r1 in matrix:
	for r2 in r1:
		print '{:4}'.format(r2),
	print
print "average distance", sum(distlist)/len(distlist)
infile.close()