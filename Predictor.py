import time
import glob
import random
import os.path
import math
import sys
from collections import defaultdict

class Predictor:

    classes = []

    '''
    Predictor which will do prediction on emails
    '''
    def __init__(self, spamFolder, hamFolder):
        self.__createdAt = time.strftime("%d %b %H:%M:%S", time.gmtime())
        self.__spamFolder = spamFolder
        self.__hamFolder = hamFolder
        # do training on spam and ham
        self.__train__()

    def __train__(self):
        '''train model on spam and ham'''
        # the following code is only an naive example,
        # implement your own training methond here
        """Train and return a naive Bayes classifier.  
        The datastructure returned is an array of tuples, one tuple per
        class; each tuple contains the class name (same as dir name)
        and the multinomial distribution over words associated with
        the class"""
        # Set up the vocabulary for all files in the training set
        vocab = defaultdict(int)
        dirs = [self.__spamFolder, self.__hamFolder]
        for dir in dirs:
            vocab.update(self.files2countdict(glob.glob(dir+"/*")))
        # Set all counts to 0
        vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))
        
        self.classes = []
        for dir in dirs:
            print dir
            # Initialize to zero counts
            countdict = defaultdict(int, vocab)
            # Add in counts from this class
            countdict.update(self.files2countdict(glob.glob(dir+"/*")))
            #***
            # Here turn the "countdict" dictionary of word counts into
            # into a dictionary of smoothed word probabilities
            #***
            # convert to float
            # add one to numerator and denominator add num of unique keys
            # freq + 1/(total num of words) + (total num of unique words)
            total_num_words = sum(countdict.values())
            total_num_unique_words = len(countdict.keys())
            for key in countdict:
                freq = float(countdict[key])
                result = float((freq + 1.0))/float((total_num_words + total_num_unique_words))
                countdict[key] = result
            self.classes.append((dir,countdict))

    def files2countdict(self, files):
        """Given an array of filenames, return a dictionary with keys
        being the space-separated, lower-cased words, and the values being
        the number of times that word occurred in the files."""
        d = defaultdict(int)
        for file in files:
            for word in open(file).read().split():
                d[word.lower()] += 1
        return d

    def predict(self, filename):
        '''Take in a filename, return whether this file is spam
        return value:
        True - filename is spam
        False - filename is not spam (is ham)
        '''
        answers = []
        print 'Classifying', filename
        for c in self.classes:
            score = float(0)
            #***
            # Here, compute the naive bayes score for a file for a given class by:
            # 1. Reading in each word, and converting it to lower case (see code below)
            # 2. Adding  the log probability of that word for that class
            #***
            # for word in nltk.word_tokenize(open(filename).read()):
            for word in open(filename).read().split():
                prob = c[1][word.lower()]
                if prob > 0:
                    val = math.log(prob)
                    score = score + val
            answers.append((score,c[0]))
        answers.sort()
        if answers[-1][1] == 'spam':
            return True
        else:
            return False
