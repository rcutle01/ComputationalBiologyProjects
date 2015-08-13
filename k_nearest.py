#
#       Implementation of k-nearest neighbors algorithm
#       Comp 167: hw 5
#       Written by: Becky Cutler
# -*- coding: utf-8 -*-

import numpy as np
import collections, sys,string, argparse, re
from collections import OrderedDict
import string, math, operator, sys, os
from scipy import stats


# reading in the data, either the test or training data, and parsing through it
def load_data(input):

        f = open(input, 'r')
        lines = f.readlines()
      
        temp = lines[0].split()
        num_genes = int(temp[0])
        c0_samples = int(temp[1])
        c1_samples = int(temp[2])
        
        data = [[0 for x in range(num_genes)] for x in range(c0_samples +
                                                             c1_samples)]

        for i in range(num_genes):
                temp = lines[i+1].split()
                for j in range(c0_samples + c1_samples):
                        data[j][i] = float(temp[j])
        return num_genes, c0_samples, data

# calculates the euclidean distance between 2 points 
def euclidean_distance(point1, point2, length):
        
        distance = 0
        for i in range(length):
                distance += pow((point1[i] - point2[i]), 2)

        return math.sqrt(distance)

#determines the k nearest neighboor based on the euclidean distance
def nearest_neighbor(test, training, k, num_samples, test_genes):

        test_length = len(test)
        nearest_distances = {};

        for i in range(test_length):
                for j in range(len(training)):
                        distance = euclidean_distance(test[i], training[j],
                        test_genes)
                        nearest_distances[j] = distance
                # now we have to sort the distances 
                nearest_neighbors = sorted(nearest_distances, 
                                           key=nearest_distances.__getitem__) 
                c0_count = 0
                c1_count = 0

                # out of all of the distances calculated, find the k-nearest
                for x in range(k):
                        # we know its in the C0
                        if nearest_neighbors[x] < num_samples: 
                                c0_count += 1
                        else:
                                c1_count += 1
                if (c0_count > c1_count):
                        sys.stdout.write('0')
                else:
                        sys.stdout.write('1')

                sys.stdout.write(' ')

def tTest(test, training, k, num_samples, test_genes):

        test_length = len(test)
        t_vals = {};

        for i in range(test_length):
               for j in range(len(training)):
                        ttest = stats.ttest_ind(test[i], training[j])
                        t_vals[j] = ttest
               sorted_vals = sorted(t_vals, key=t_vals.__getitem__)

               c0_count = 0
               c1_count = 0

                # out of all of the distances calculated, find the k-nearest
               for x in range(k):
                                # we know its in the C0
                       if sorted_vals[x] < .03: 
                               c0_count += 1
                       else:
                               c1_count += 1
               if (c0_count > c1_count):
                       sys.stdout.write('0')
               else:
                       sys.stdout.write('1')

               sys.stdout.write(' ')



################ main implementation###############
# first, get the files,  we need one file for the
# training data, and one file for the test data

#getting the arguments from the user 
parser = argparse.ArgumentParser(description= 'K-nearest neighbor.')
parser.add_argument('test_input', help= 'file for the query reads')
parser.add_argument('training_input', help= 'file for the training reads')
parser.add_argument('-k', type=int, help= 'amount of nearest neighbors')

args = parser.parse_args()
test_data = args.test_input
training_data = args.training_input
k = args.k

# parse through the file and create a 2D array of data
train_genes, num_test_samps, test_data = load_data(test_data)
test_genes, num_train_samps, training_data = load_data(training_data)


nearest_neighbor(test_data, training_data, k, num_train_samps, test_genes)
        
#tTest(test_data, training_data, k, num_train_samps, test_genes)

