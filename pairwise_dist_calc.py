from Bio import AlignIO
import sys
import glob

inputfolder = sys.argv[1]
files = glob.glob(inputfolder+"/*.fas")
for f in files:
	aln = AlignIO.read(open(f), "fasta")
	for seq in aln:
		seq.seq = seq.seq.upper()
	length = aln.get_alignment_length()
	bait_gap = 0
	target_gap = 0
	mismatch = 0
	match = 0
	for pos in range(length):
		if aln[0][pos] == "-":
			bait_gap += 1
		elif aln[1][pos] == "-":
			target_gap += 1
		else:
			if aln[0][pos] == aln[1][pos]:
				match += 1
			else:
				mismatch += 1
	pc_match = str(round(match / float(length) * 100, 3))
	pc_mismatch = str(round(mismatch / float(length) * 100, 3))
	pc_bait_gap = str(round(bait_gap / float(length) * 100, 3))
	pc_target_gap = str(round(target_gap / float(length) * 100, 3))
	print f+'\t'+pc_match+'\t'+pc_mismatch+'\t'+pc_bait_gap+'\t'+pc_target_gap