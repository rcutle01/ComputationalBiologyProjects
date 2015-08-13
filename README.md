# SequenceAssembler
Python program that implements a de Bruijn graph to assemble a sequence of contigs

README file for assembler.py for Comp 167 hw2
    written by: Becky Cutler (rcutle01)
    2.17.15

Summary: This program aims to separate a given file of sequence into its respective kmers 
         and from these nodes, build a de Bruijin graph. This graph is then 
         analyzed so that only the "good" sequence reads are used to build 
         the graph. Using these "good" reads, the graph is rebuilt wit the
         correct kmers. From this graph, contigs are made by walking various
         paths. These contigs are then outputted to a file called output_contig.

How to compile/run
type the command:
python assembler.py <FILE NAME> -k <KMER SIZE>

Approx time to run with the sequence_reads file: 4 minutes 
