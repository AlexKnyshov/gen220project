from Bio import Phylo
import os
import sys
import glob
if len(sys.argv) == 3:
	files = glob.glob(sys.argv[2]+"/*.tre")
	opt = sys.argv[1]
else:
	print "FORMAT: python treeprocsep.py [option: -75, -avg] [folder with trees]"
	print "EXAMPLE: python treeprocsep.py -75 ./trees"
	sys.exit()
if len(files) == 0:
	print "no trees in the directory"
#starting to process files
progbarc = 0
result = {}
#test
for f in files:
	print f
	tree = Phylo.read(f, "newick")
	#tree = Phylo.read("./../testtree.tre", "newick")
	if tree.is_bifurcating():
		print "bifurcating"
	else:
		print "not bifurcating"
	counter = 0
	ct = 0
	test = tree.as_phyloxml()
	list4 = test.find_clades()
	totconf = 0
	lowconf = 0
	conflist = []
	for l1 in list4:
		counter +=1
		if l1.is_bifurcating():
			ct +=1
		l2 = str(l1._get_confidence())
		if l2.find("Confidence") == 0:
			totconf +=1
			l3=l2.split(",")
			l4 = l3[1][:-1].split("=")
			if opt == "-75":
				if int(l4[1]) <75:
					lowconf +=1
			elif opt == "-avg":
				conflist.append(int(l4[1]))
	print "below 70 per cent", float(lowconf)/(totconf)
	print "clades #", counter, ct
	fname = f.split("/")[2]
	tr = fname.split(".")[1]
	if opt == "-75":
		result[tr] = float(lowconf)/(totconf)
	elif opt == "-avg":
		result[tr] = float(sum(conflist)/len(conflist))
	#progress bar
	progbarc +=1
	progbar = int(round(float(progbarc)/len(files)*100, 0))
	hashes = '#' * int(progbar * 0.2)
	spaces = ' ' * (20 - len(hashes))
	print "-------------------------------------"
	print "\rProgress: [{0}] {1}%".format(hashes + spaces, progbar)
	print "-------------------------------------"
#output the final table
with open("treesfilter.tab", "w") as outfile:
	for tc, tcv in result.items():
		print >> outfile, tc, "\t", tcv
print "Done"