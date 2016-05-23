from Bio import AlignIO
from Bio.Alphabet import IUPAC, Gapped
from Bio.Seq import Seq 
from Bio.SeqRecord import SeqRecord 
from Bio.Align import MultipleSeqAlignment

import sys
import glob
import os

if len(sys.argv) >= 5:
	inputfolder = sys.argv[1]
	partnum = sys.argv[2]
	phyliptype = sys.argv[3]
	pf2opt = sys.argv[4]
	if len(sys.argv) == 6:
		exclusion_file = sys.argv[5]
else:
	print "FORMAT: python concat.py [folder with fasta] [split to codon positions: -3 (yes), -1 (no)] [partition_finder output: -pf2y, -pf2n] [phylip type: -i (interleaved), -s (sequential)] ([exclusion list])"
	print "EXAMPLE: python concat.py ./fasta -1 -i -pf2n"
	print "EXAMPLE: python concat.py ./fasta -1 -s -pf2y list.lst"
	print "output is written to COMBINED.phy, partitions are written to partitions.prt"
	sys.exit()

exclusion_list = []
if len(sys.argv) == 6:
	print "reading exclusion list..."
	exfile = open(exclusion_file, "r")
	for line in exfile:
		l = line.strip()
		exclusion_list.append(l)
	exfile.close()
	print "read", len(exclusion_list), "records"

print "creating a list of taxa..."
d = {}
files = glob.glob(inputfolder+"/*.fas")
for f in files:
	fnew = f.split("/")
	fn = fnew[len(fnew)-1]
	alignment = AlignIO.read(f, "fasta", alphabet=Gapped(IUPAC.ambiguous_dna))
	length = alignment.get_alignment_length()
	for seq in alignment:
		if seq.id in d and seq.id not in exclusion_list:
			d[seq.id].append(fn)
		elif seq.id not in exclusion_list:
			d[seq.id] = []
			d[seq.id].append(fn)
print len(d), "taxa found in fasta alignments"

print "concatenating..."
oks = 0
skips = 0
align = MultipleSeqAlignment([], Gapped(IUPAC.ambiguous_dna)) # new ali
for dx in d.keys():
	align.append(SeqRecord(Seq("", Gapped(IUPAC.ambiguous_dna)), id=dx)) #add taxa
#print align
counter = 0
outputfile = open("partitions.prt", "w")
if pf2opt == "-pf2y":
	pf2cfg = open("partition_finder.cfg", "w")
 	print >> pf2cfg, "alignment = COMBINED.phy;"
 	print >> pf2cfg, "branchlengths = linked;"
 	print >> pf2cfg, "models = all;"
 	print >> pf2cfg, "model_selection = BIC;"
 	print >> pf2cfg, "[data_blocks]"
for f in files:
	temp = MultipleSeqAlignment([], Gapped(IUPAC.ambiguous_dna)) #temp ali
 	fnew = f.split("/")
 	fn = fnew[len(fnew)-1]
 	alignment = AlignIO.read(f, "fasta", alphabet=Gapped(IUPAC.ambiguous_dna)) #read original
 	length = alignment.get_alignment_length()
	missed = list(d)
 	for seq in alignment:
 		temp.append(seq) #add original to temp
 		if seq.id in missed:
 			missed.remove(seq.id)
 	for m in missed:
 		temp.append(SeqRecord(Seq("?"*length, Gapped(IUPAC.ambiguous_dna)), id=m)) #add dummies
 	counter = 0
 	temp2 = MultipleSeqAlignment([], Gapped(IUPAC.ambiguous_dna))
 	for aliseq in align:
 		for tempseq in temp:
 			if aliseq.id == tempseq.id:
 				temp2.append(aliseq + tempseq)
 	start = align.get_alignment_length()+1
 	end = align.get_alignment_length()+length
 	prog = "working on partition "+str(fn)+": starts "+str(start)+", ends "+str(end)
 	sys.stdout.write(prog+"\r")
 	sys.stdout.flush()
 	align = temp2
 	counter += align.get_alignment_length()
 	if pf2opt == "-pf2y":
 		if partnum == "-3":
			print >> pf2cfg, fn[:-4]+"_1 = "+str(start)+" - "+str(end)+"\\3;"
			print >> pf2cfg, fn[:-4]+"_2 = "+str(start+1)+" - "+str(end+1)+"\\3;"
			print >> pf2cfg, fn[:-4]+"_3 = "+str(start+2)+" - "+str(end+2)+"\\3;"
		elif partnum == "-1":
			print >> pf2cfg, fn[:-4]+" = "+str(start)+" - "+str(end)+";"
 	if partnum == "-3":
		print >> outputfile, "DNA, "+fn+"-1 = "+str(start)+" - "+str(end)+"\\3"
		print >> outputfile, "DNA, "+fn+"-2 = "+str(start+1)+" - "+str(end)+"\\3"
		print >> outputfile, "DNA, "+fn+"-3 = "+str(start+2)+" - "+str(end)+"\\3"
	elif partnum == "-1":
	 	print >> outputfile, "DNA, "+fn+" = "+str(start)+" - "+str(end)
if pf2opt == "-pf2y":
	print >> pf2cfg, "[schemes]"
	print >> pf2cfg, "search = greedy;"
	pf2cfg.close()
outputfile.close()
print "\ndone"

print "writing..."
if phyliptype == "-i":
	AlignIO.write(align, "COMBINED.phy", "phylip-relaxed")
elif phyliptype == "-s":
	outf = open("COMBINED.phy", "w")
	print >> outf, str(len(align))+" "+str(align.get_alignment_length())
	for seq in align:
		print >> outf, str(seq.id)+" "+str(seq.seq)
	outf.close()
print "done"
