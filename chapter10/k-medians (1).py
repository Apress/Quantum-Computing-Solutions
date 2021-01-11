

import numpy as nump
from k_medians_utils import *


PREFIX = ''

FILE = PREFIX + 'iris.data.txt'

[xval, yval] = read(FILE)


[n, d] = nump.shape(xval)   
k = len(nump.unique(yval))  

mi = nump.min(xval, axis=0) 
ma = nump.max(xval, axis=0) 
di = ma - mi           
stop = 0               

c = nump.zeros(n)         
median = nump.random.rand(k, d) * nump.ones((k, d)) 
median = median * di
median = median + mi
med_t = nump.copy(median) 

imax = 100
for i in range(imax):
   med_t = nump.copy(median)
  

   for j in range(n):
      dist = nump.sqrt(nump.sum(nump.power(xval[j,:] - median, 2), axis=1))
      idx = nump.argmin(dist)
      val = nump.min(dist)
      c[j] = idx
   
   for j in range(k):
      a = nump.arange(n)
      idx = a[c == j] 
      l = len(idx)   
      if l:
         median[j,:] = nump.median(xval[idx,:], axis=0)
      else:
         median[j,:] = median[j,:] + (nump.random.rand(d) * di)

   stop = nump.sum(nump.sum(nump.power(median - med_t,2), axis=0))
   if(stop <= 0) or (i >= imax):
      break

accur = getAccuracy(c, yval, k)
silhou = getSilhouette(xval, c, median)
print(accur, silhou)