# -*- coding: utf-8 -*
# Implementation file for a sequence assembler using a de Bruijin graph
# computational biology 
# writen by: Becky Cutler (rcutle01)
# 2/17/15

import collections, sys,string, argparse, re
from collections import OrderedDict
import string 

#DeBruijin graph node with associated info
class dbNode:
        def __init__(self,kmer_seq,full_seq):
                self.kmer = kmer_seq
                self.outedg = [] # outgoing edge
                self.inedg = [] #incoming edge
                self.marker = 0
                self.branch = 0
                self.sequence = full_seq
                #num times the node's string appears in the reads you 
                #are proecssing
                self.numAppear = 0
                self.beg = 0
                self.end = 0
                
#holds the individual sequence reads as a node            
class seq_read:
        def __init__(self, sequence):
                self.read = sequence

                    
# DeBruijin graph that holds k-mer nodes, and can iterate through
# them and add them
class dbGraph:
        def __init__(self):
                self.graph = OrderedDict()
        def add(self, prev, cur, next, read):
                new_node = dbNode(cur, read)
                #checking the 3 cases:
                #if next is NULL
                if next == 0:
                        if cur not in self.graph: #ie if its not in the graph
                                # adding it to the graph
                                self.graph[cur] = new_node
                                self.graph[cur].numAppear = 1
                        else:
                                self.graph[cur].numAppear += 1
                        if prev != 0: # if prev exists, check to see if its 
                                       # an incoming edge
                                if not prev in self.graph[cur].inedg:
                                       self.graph[cur].inedg.append(prev)
                # if prev is NULL                      
                elif prev == 0:
                        if cur not in self.graph: 
                                # adding it to the graph
                                self.graph[cur] = new_node
                                self.graph[cur].numAppear = 1
                        else: 
                                self.graph[cur].numAppear += 1 
                                #checking to see if it has an outgoing edge
                        if not next in self.graph[cur].outedg:
                                self.graph[cur].outedg.append(next)
                                
                # if neither is NULL
                else:
                        if cur not in self.graph:
                                # adding it to the graph
                                self.graph[cur] = new_node
                                self.graph[cur].numAppear = 1
                        else:
                               self.graph[cur].numAppear += 1 
                       #checking to see if it has an incomming edge
                        if not prev in self.graph[cur].inedg:
                               self.graph[cur].inedg.append(prev)
                       #checking it see if it has an outgoing edge
                        if not next in self.graph[cur].outedg:
                               self.graph[cur].outedg.append(next)

# sequence reads graph
class seqGraph:
        def __init__(self):
                self.graph = OrderedDict()
        def add(self,sequence):
                if not sequence in self.graph:
                        new_node = seq_read(sequence)
                        self.graph[sequence] = new_node
        def remove(self,sequence):
                if sequence in self.graph:
                        del self.graph[sequence] 

# read_file: using the given file, it stores kmers depending on the 
#given kmer size
def read_file(given_file):
        file = open(given_file, 'r')
        
        #for each line in the file
        for line in file:
                line = string.replace(line, '\n', '')
                length = len(line)
                prev = 0;
                seqGraph.add(line)

                #devide the line into k-mers
                for i in range(0, length):
                        if i + kmer_sz <= length: # making sure in range 
                                if i + kmer_sz + 1 <= length: # getting the next
                                                              # kmer
                                        next = line[i + 1: i + kmer_sz + 1]
                                else: # the next kmer will be out of bounds 
                                        next = 0
                                #setting the current kmer
                                cur = line[i: (kmer_sz + i)]
                                dbGraph.add(prev, cur, next, line)
                                prev = cur
        file.close() 

        #checking for branches, beginning, and end Nodes
        for key, value in dbGraph.graph.items():
                if len(value.inedg) > 1 or len(value.outedg) > 1:
                        value.branch = 1
                if len(value.inedg) == 0:
                        value.beg = 1
                if len(value.outedg) == 0:
                        value.end = 1
                
# walks through the graph and removes verticies that appear only once
#then it outputs these good reads to the correct file 
def analyzeGoodReads(dbGraph, seqGraph):
        for key, value in dbGraph.graph.items():
                if value.numAppear == 1: #if the kmer is only found once in
                                         #the graph
                        #remove the sequence
                        seqGraph.remove(value.sequence)
                if len(value.outedg) > 1 or len(value.inedg) > 1:
                        value.branch = 1

        f = open('good_reads', 'w')
        for key, value in seqGraph.graph.items():
                f.write(value.read + '\n')

        f.close
        dbGraph.graph.clear() # deleting previous graph which contains 
                              # sequences that arent "good reads"

# rebuilds the graph with the new good_reads file
def rebuild_dbgraph():
      new_file = 'good_reads'
      read_file(new_file)

def assemble(dbGraph):

        contig = []
        #find the beginning node
        for key, value in dbGraph.graph.items():
                if value.beg == 1: # found a beginning node
                        temp = buildcontig(value, dbGraph)
                        if len(temp) > 1: #checking for the right size
                                contig.append(temp)

        for key, value in dbGraph.graph.items():
                if value.marker == 0: # if its an unmarked node
                        if value.branch == 1: # and branched
                                continue
                        # if inedge is a branch- we've found a new starting point 
                        if dbGraph.graph[value.inedg[0]].branch == 1:
                                temp = buildcontig(value,dbGraph)
                                if len(temp) > 1: #checking for the right size
                                        contig.append(temp)
        return contig

def buildcontig(value, dbGraph): 

        temp = value.kmer
        value.marker = 1
        if value.end == 1:
                return temp
        value = dbGraph.graph[value.outedg[0]]
        while(1):
                if value.branch == 1: # weve found a branch node
                        value.marker = 1
                        temp += value.kmer[-1:]
                        break
                if value.marker == 1:
                        break
                temp += value.kmer[-1:] #getting the last char of the kmer
                value.marker = 1 # mark it 
                if value.end == 0:
                        value = dbGraph.graph[value.outedg[0]] # get the next edge     
                else:
                        break
        return temp

def outPutContigs(contigs):

        of = open('output_contigs', 'w')
        oflen = open('contig_lengths','w')
        for value in contigs: # looping through the contigs
                of.write(value + '\n')
                oflen.write(str(len(value)) + '\n')

        of.close
        oflen.close

#creating the two graphs:       
dbGraph = dbGraph()
seqGraph = seqGraph()

#getting the arguments from the user 
parser = argparse.ArgumentParser(description= 'Sequence assembler.')
parser.add_argument('input_file', help= 'file for the sequence reads')
parser.add_argument('-k', type=int, help= 'the length of k-mers')

args = parser.parse_args()
seq_file = args.input_file
kmer_sz = args.k

# GENERAL IMPLEMENTATION:
read_file(seq_file)
analyzeGoodReads(dbGraph,seqGraph)
rebuild_dbgraph()
outPutContigs(assemble(dbGraph))
