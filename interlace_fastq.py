import sys


if len(sys.argv) == 4:
	readname1 = sys.argv[1]
	readname2 = sys.argv[2]
	mode = sys.argv[3]

else:
	print "FORMAT: argument1 = read1, argument2 = read2, mode = b (use biopython) or t (simple text mode)"
	print "EXAMPLE: read1.fq read2.fq b"
	print "EXAMPLE: read1.fq read2.fq t"
	print "output is written to readsN.fq"
	sys.exit()
bucket = 0
readcount = 0
if mode == "b":
	from Bio import SeqIO
	readhandle1 = open(readname1)
	read1 = SeqIO.parse(readhandle1, "fastq")
	read2 = SeqIO.index(readname2, "fastq")
	readhandle3 = open("reads.fq","w")
	for seq in read1:
		SeqIO.write(seq, readhandle3, "fastq")
		SeqIO.write(read2[seq.id[:-2]+"/2"], readhandle3, "fastq")
	readhandle1.close()
	readhandle3.close()
else:
	readhandle1 = open(readname1)
	readhandle2 = open(readname2)
	readhandle3 = open("reads"+str(bucket)+".fq","w")
	r2lines = []
	for r1line in readhandle1:
		if len(r2lines) < 4:
			print >> readhandle3, r1line.strip()
			r2lines.append(readhandle2.next().strip())
		else:
			for r2line in r2lines:
				print >> readhandle3, r2line
			r2lines = []
			print >> readhandle3, r1line.strip()
			r2lines.append(readhandle2.next().strip())
		if readcount == 1000000:
			readhandle3.close()
			bucket += 1
			readhandle3 = open("reads"+str(bucket)+".fq","w")
	if len(r2lines) == 4:
		for r2line in r2lines:
			print >> readhandle3, r2line
	readhandle1.close()
	readhandle2.close()
	readhandle3.close()