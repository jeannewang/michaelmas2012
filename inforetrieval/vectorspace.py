"""documents are vectors
queries are vectors

create a vector of terms

have a inverted index: term->(freq,docid)

cosine distance measure

tfidf
"""
import os
from numpy import *
     
docPath = '/usr/local/practicals/ir/practical1/docs/'
documentNames = os.listdir(docPath)

documentVectors=dict() #holds docName to docVector

termToDocFreq = dict() #holds term to document frequency mapping
termToTermFreq = dict() #holds term to (docName, term freq) mapping

#read in the inverted index to get termToDocFreq and termToTermFreq
invertedIndexPath='/usr/local/practicals/ir/practical1/data/index.txt'
ii = open(invertedIndexPath,'r')
ii = ii.readlines()

for line in ii:
  line = line.split(' ')
  term = line[1]
  docFreq = line[2]
  termToDocFreq[term]=int(docFreq)
  termToTermFreq[term]=[]
  line = line[3:]
  for i in range(0,len(line),2):
    docName=line[i]
    termFreq=int(line[i+1])
    termToTermFreq[term].append((docName,termFreq))

termVector = termToDocFreq.keys()
numTerms = len(termVector)

#Create the document vectors
for dName in documentNames:
  d = open(docPath+dName, 'r')
  d = d.read().split(' ')
  documentVectors[dName]=zeros(numTerms)
  for token in d:
    if(token in termVector):
      termFreqList=termToTermFreq[token]
      tf=filter(lambda (x,y): x==dName,termFreqList)
      tf=tf[0][1]
      idf=1/termToDocFreq[token]
      documentVectors[dName][termVector.index(token)]=tf*idf

#Create the query vector      
query=['financial','instruments','being','traded','American','stock','exchange']

queryVector=zeros(numTerms)
for q in query:
  queryVector[termVector.index(q)]=1


def cosineDist(A,B):
  return dot(A,B) / linalg.norm(A)*linalg.norm(B)

result=[]
for dName in documentVectors.keys():
  d=documentVectors[dName]
  dist=cosineDist(d,queryVector)
  result.append((dist,dName))

result=(result.sort()).reverse()
print result
open('result.txt', 'w').write('\n'.join('%s %s' % x for x in result))



