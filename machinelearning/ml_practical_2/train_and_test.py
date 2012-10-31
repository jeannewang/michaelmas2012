#!/usr/bin/env python
"""
Machine Learning Practical 2: train_and_test.py

usage: python train_and_test.py [option]
Options and arguments:
  -h, --help                         : print this help message
  -i, --iterations=arg               : max number of training iterations
  -n, --eta=arg                      : eta step size parameter in 
                                       gradient descent
  -t, --threshold=arg                : gradient tolerance termination 
                                       parameter for BFGS
  -r, --regularisation-parameter=arg : Gaussian sigma^2 parameter in the 
                                       logistic regression MAP objective
  -b, --bfgs                         : Use the BFGS quasi-newton optimisation
                                       algorithm instead of gradient descent
"""
import sys, getopt
import numpy as np
import scipy.optimize as op

from logreg import *
from util import *


# These three functions are helpers for the BFGS optimiser
last_func=0
iterations=0
def function(w, x, t, r): 
  global last_func
  last_func = sum(objective(x,t,w)) + log_prior(w, r)
  return last_func

def function_grad(w, x, t, r): 
  return grad(x,t,w)+prior_grad(w, r) 

def report(w):
  global last_func
  global iterations
  if not (iterations % 10):
    print '   iteration', iterations, ': cross entropy=', last_func
  iterations += 1


# This is the main function for training and testing the logistic 
# regression model.
def experiment(cmdline_args):
  # read the data
  data = np.genfromtxt('./data/cs-training_mod.csv', delimiter=',')
  test_data = np.genfromtxt('./data/cs-test_mod.csv', delimiter=',')

  # drop the first header row
  data = data[1:]
  test_data = test_data[1:]

  N, K = data.shape
  D = 1 # the target classification is the second column
  K = K-D-1

  # Hold aside 1/10 of the training data for calculating the heldout AUC
  training, development = split_data(10, 9, data)

  # the last K columns are the features
  x = training[:,-K:]
  xdev = development[:,-K:]
  xtest = test_data[:,-K:]

  # the second column is the response variable
  t = training[:,D]
  tdev = development[:,D]

  #################################################
  # TODO: you should transform x, xdev, and xtest 
  #       here...
  #################################################

  #################################################

  # initialise the model weights to zero
  w = np.zeros(x.shape[1], 'f')

  if cmdline_args['bfgs']:
    # Use the quasi-Newton convex optimisation algorithm BFGS from Scipy. It's much more 
    # effective than gradient descent.
    # BFGS is an iterative algorithm which calls function(w) and function_grad(w) on each iteration 
    # to calculate the objective function and its gradient. The function report(w) is also called
    # to enable the progress of the optimisation to be reported to stdout. gtol is the gradient
    # tolerance, if the norm of the gradient doesn't change by at least this much between 
    # iterations the optimiser will terminate.
    print "Optimising with BFGS:"
    w = op.fmin_bfgs(function, w, args=(x,t,cmdline_args["regularisation"]), fprime=function_grad, \
                     callback=report, maxiter=cmdline_args["iterations"], \
                     gtol=cmdline_args["threshold"])
  else: # otherwise use gradient descent
    print "Optimising with Gradient Descent:"
    for i in range(cmdline_args["iterations"]):
      w -= cmdline_args["eta"] * function_grad(w, x, t, cmdline_args["regularisation"]) 
      if not (i% 10):
        print '   iteration', i, ': cross entropy=', function(w, x, t, cmdline_args["regularisation"])

  print '\nFinal training cross entropy', sum(objective(x, t, w))
  print 'Final heldout cross entropy', sum(objective(xdev, tdev, w))

  # Use the learnt model to assign probabilities to each training and development point
  probs = np.exp(log_sigmoid(np.dot(x, w)))
  dev_probs = np.exp(log_sigmoid(np.dot(xdev, w)))

  # AUC calculation
  print '\nTraining AUC', AUC(t,probs)
  print 'Heldout development AUC', AUC(tdev,dev_probs)

  # Use the learnt model to assign probabilities to each test point
  test_probs = np.exp(log_sigmoid(np.dot(xtest, w)))

  # label the test data using the learnt feature weights w
  out = open(cmdline_args['test-out'],'w')
  for i,p in enumerate(test_probs):
    print >>out,'%d,%f' % (i+1,p)
  out.close()


"""
Utility exception for generating a help message.
"""
class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


"""
This is an example main function for your experiment.
It demonstrates how to initialise and parse command
line arguments and then call the specific experiment
function.
"""
def main(argv=None):
  experiment_args = {}
  experiment_args["iterations"] = 1000
  experiment_args["eta"] = 1e-11
  experiment_args["regularisation"] = 10
  experiment_args["threshold"] = 1e1
  experiment_args["bfgs"] = False
  experiment_args["test-out"] = "logreg-entry.csv"

  # Example command line argument processing.
  # You can add any arguments you see fit. 
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hi:n:r:t:bo:", 
                                 ["help",
                                  "iterations=",
                                  "eta=",
                                  "threshold=",
                                  "test-out=",
                                  "bfgs",
                                  "regularisation-parameter="])
    except getopt.error, msg:
      raise Usage(msg)

    # process options
    for option, argument in opts:
      if option in ("-h", "--help"):
        print __doc__
        sys.exit(0)
      if option in ("-i", "--iterations"):
        experiment_args["iterations"] =int(argument)
      if option in ("-n", "--eta"):
        experiment_args["eta"] = float(argument)
      if option in ("-t", "--threshold"):
        experiment_args["threshold"] = float(argument)
      if option in ("-r", "--regularisation-parameter"):
        experiment_args["regularisation"] = float(argument)
      if option in ("-o", "--test-out"):
        experiment_args["test-out"] = argument
      if option in ("-b", "--bfgs"):
        experiment_args["bfgs"] = True

  except Usage, err:
    print "Error parsing command line arguments:"
    print >>sys.stderr, "  %s" % err.msg
    print __doc__
    return 2
  
  # run our experiment function
  experiment(experiment_args)


# This is how python handles main functions.
# __name__ won't equal __main__ be defined if 
# you import this file rather than run it on 
# the command line.
if __name__ == "__main__":
  sys.exit(main())
