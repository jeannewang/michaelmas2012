import sys, numpy, inspect


def todo():
  print "You should implement this function: %s" % inspect.stack()[1][3]
  sys.exit(1)


"""
Split data into 'splits' different sub-blocks, returning the
block indexed by 'test_split' plus the rest of the data.
"""
def split_data(splits, test_split, data):
  assert test_split >= 0 and test_split < splits
  assert splits <= len(data)

  split_size = len(data) / int(splits)
  test_start = split_size*test_split
  test_end   = test_start + split_size

  test  = data[test_start:test_end]
  train = numpy.concatenate([data[0:test_start],data[test_end:]])

  return (train,test)


"""
Python re-implementation of Matlab tiedrank function 
"""
def tiedrank(X):  
  Z = [(x, i) for i, x in enumerate(X)]  
  Z.sort()  
  n = len(Z)  
  Rx = [0]*n   
  for j, (x,i) in enumerate(Z):  
    Rx[i] = j+1  
  s = 1           # sum of ties.  
  start = end = 0 # starting and ending marks.  
  for i in range(1, n):  
    if Z[i][0] == Z[i-1][0] and i != n-1:  
      pos = Z[i][1]  
      s+= Rx[pos]  
      end = i   
    else: #end of similar x values.  
      tiedRank = float(s)/(end-start+1)  
      for j in range(start, end+1):  
        Rx[Z[j][1]] = tiedRank  
      for j in range(start, end+1):  
        Rx[Z[j][1]] = tiedRank  
      start = end = i  
      s = Rx[Z[i][1]]    
  return Rx


"""
Python re-implementation of Kaggle's Matlab AUC code
"""
def AUC(labels, posterior):
  r = tiedrank(posterior)
  auc = (sum(r*(labels==1)) - sum(labels==1)*(sum(labels==1)+1)/2) / (sum(labels<1)*sum(labels==1));
  return auc
