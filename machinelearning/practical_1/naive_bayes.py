#!/usr/bin/env python
"""
Machine Learning Practical 1: Naive Bayes for text classification

usage: python naive_bayes.py [option]
Options and arguments:
  -h, --help                         : print this help message
  -s, --stop                         : filter out stop words
  -a, --alpha                        : Dirichlet prior parameter 
                                       for the p(C) distribution
  -b, --beta                         : Dirichlet prior parameter 
                                       for the p(word|C) distributions
  -d, --data-dir                     : data directory containing 'neg' 
                                       and 'pos' sub-dirs with the 
                                       training documents as individual 
                                       files
  -i, --cross-validation-iterations  : repeat the experiment i times 
"""
# useful system libraries
import os, sys, getopt, inspect
from collections import defaultdict

# core mathematic libraries
from math import log
from random import shuffle 

# This file contains a list of stopwords
from stopwords import *

def todo():
  print "You should add code here: Function %s, Line %s." \
    % (inspect.stack()[1][3], inspect.stack()[1][2])
  sys.exit(1)

"""
This is the core experiment function which contains a 
simple implementation of Naive Bayes training and testing
description.
"""
def experiment(args):
  pos_path = args["data_dir"] + "/pos/" 
  neg_path = args["data_dir"] + "/neg/" 

  # read the list of document files into a list and randomise 
  # their order. This uses python's list comprehensions.
  files = [("pos",pos_path+x) for x in os.listdir(pos_path)] \
        + [("neg",neg_path+x) for x in os.listdir(neg_path)]
  shuffle(files)

  # now we partition the data, one set for testing and the
  # other for training. list[:n] returns the first n elements
  # in a list and list[n:] drops the first n elements.
  training_files = files[:len(files)*4/5]
  test_files = files[len(files)*4/5:]

  # Training: visit each training file and count the number 
  # of times we saw a word and with a class, and the number
  # of times we saw the class. 'defaultdict(int)' is a 
  # dictionary type for which querying keys not present returns
  # 0, useful for counters.
  count_pos_words = defaultdict(int) # count(word, C=pos)
  count_neg_words = defaultdict(int) # count(word, C=neg)
  count_class = defaultdict(int)     # count(C)
  unique_words = set()
  num_training_files = len(training_files)

  for label,file in training_files:
    count_class[label] += 1
    for line in open(file):
      for token in line.split():
        if not args["stopwords"] or token not in stopwords:
          unique_words.add(token)
          if label == "pos": count_pos_words[token] += 1
          else:              count_neg_words[token] += 1

  # Count the total number of words for each class.
  # 'reduce' is pythons equivalent of Haskell's 'foldl1'
  # and 'lambda' declares an unnamed function.
  pos_words = reduce(lambda x,y: x+y, count_pos_words.values())
  neg_words = reduce(lambda x,y: x+y, count_neg_words.values())
  num_unique_words = len(unique_words)

  def pmapWord(word, Ck, beta):
    if Ck=="pos":
      retValueTop=(beta-1)+count_pos_words[word]
      retValueDivisor=num_unique_words*(beta-1)+pos_words
    else:
      retValueTop=(beta-1)+count_neg_words[word]
      retValueDivisor=num_unique_words*(beta-1)+neg_words
    return log(retValueTop)-log(retValueDivisor)
 
  def pmapCategory(Ck, alpha):
    if Ck=="pos":
      retValueTop=(alpha-1)+count_class["pos"]
    else:
      retValueTop=(alpha-1)+count_class["neg"]
    retValueDivisor=num_training_files+2*(alpha-1)
    return log(retValueTop)-log(retValueDivisor)

    
  # Testing: visit each testing file and calculate its
  # predicted class given the score: 
  #     argmax log p(words|C) + log p(C)
  # Note that calculating scores in log space reduces the
  # risk of floating point underflow, however zeros will
  # cause an exception. 
  correct_predictions=0
  for label,file in test_files:
    pos_score = 0
    neg_score = 0

    # calculate log p(C) score contributions, 
    pos_score=pmapCategory("pos",args["alpha"])
    neg_score=pmapCategory("neg",args["alpha"])
    
    for line in open(file):
      for token in line.split():
        if not args["stopwords"] or token not in stopwords:
          # calculate the log p(word|C) score contributions
	  pos_score+=pmapWord(token,"pos",args["beta"])
 	  neg_score+=pmapWord(token,"neg",args["beta"])
    if pos_score >= neg_score and label == 'pos':
      correct_predictions += 1
    elif pos_score < neg_score and label == 'neg':
      correct_predictions += 1

  return float(correct_predictions) / len(test_files)        



"""
This is an example main function for your experiment.
It demonstrates how to initialise and parse command
line arguments and then call the specific experiment
function.
"""
def main(argv=None):
  experiment_args = {}
  experiment_args["stopwords"] = False 
  experiment_args["alpha"] = 1
  experiment_args["beta"] = 1
  experiment_args["data_dir"] = "./review_data/"
  experiment_args["cross-validation-iterations"] = 1

  # Example command line argument processing.
  # You can add any arguments you see fit. 
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hsa:b:d:i:", 
                                 ["help",
                                  "stopwords",
                                  "alpha=",
                                  "beta=",
                                  "data_dir=",
                                  "cross-validation-iterations"])
    except getopt.error, msg:
      raise Exception(msg)

    # process options
    for option, argument in opts:
      if option in ("-h", "--help"):
        print __doc__
        sys.exit(0)
      if option in ("-s", "--stopwords"):
        experiment_args["stopwords"] = True
      if option in ("-a", "--alpha"):
        experiment_args["alpha"] = float(argument)
      if option in ("-b", "--beta"):
        experiment_args["beta"] = float(argument)
      if option in ("-d", "--data-dir"):
        experiment_args["data_dir"] = argument
      if option in ("-i", "--cross-validation-iterations"):
        experiment_args["cross-validation-iterations"] = int(argument)
  except Exception as err:
    print "Error parsing command line arguments:"
    print >>sys.stderr, "  %s" % err
    print __doc__
    return 2
  
  # run our experiment function
  average = 0
  for x in range(0,experiment_args["cross-validation-iterations"]):
    accuracy = experiment(experiment_args)
    average += accuracy
    print "   Run ", x, ": Accuracy = ", accuracy 
  print "Average Accuracy = ", \
        average / experiment_args["cross-validation-iterations"] 



# This is how python handles main functions.
# __name__ won't equal __main__ if you 
# import this file rather than run it on 
# the command line.
if __name__ == "__main__":
  sys.exit(main())
