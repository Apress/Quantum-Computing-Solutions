
import numpy as nump
import os

VERBOSE = False

def read(FILE):
   if os.path.isfile(FILE):
      file = open(FILE, 'r')
      lines = tuple(file)
      file.close()
      data = []
      for line in lines:
         data.append(line.rstrip().split(","))
         if VERBOSE:
            print(data[-1])
   else:
      print(FILE, 'does not exist')
      exit(0)

   data = nump.array(data)
   x = data[:,0:-1]
   x = x.astype(nump.float)

   y = nump.zeros(len(data))
   uniq = nump.unique(data[:,-1])
   for i in range(0,len(uniq)):
      idx = (data[:,-1] == uniq[i])
      if any(idx):
         y[idx] = i

   return(x, y)

def getAccuracy(c, y, k):
   if VERBOSE:
      print(c)
      print(y)

   n = len(y)
   kk = nump.zeros(k)
   o = 0
   e = 0
   idxx = []
   for i in range(k):
      a = nump.arange(n)
      idxa = a[y == i]
      for j in range(len(idxa)):
         kk[int(c[j+o])] = kk[int(c[j+o])] + 1
      if idxx:
          for l in idxx:
             kk[l] = 0
      o = o + len(idxa)
      idx = nump.argmax(kk)
      idxx.append(idx)
      val = kk[idx]
      e = e + (val/len(y[y == i]))
      kk = nump.zeros(k)
   e = e/k
   return(e)


def accuracy_(c, y, k1, k2):
   if VERBOSE:
      print(c)
      print(y)

   n = len(y)
   kk = nump.zeros(k2)
   o = 0
   e = 0
   idxx = []
   for i in range(k1):
      a = nump.arange(n)
      idxa = a[y == i]
      for j in range(len(idxa)):
         kk[int(c[j+o])] = kk[int(c[j+o])] + 1
      if idxx:
          for l in idxx:
             kk[l] = 0
      o = o + len(idxa)
      idx = nump.argmax(kk)
      idxx.append(idx)	  
      val = kk[idx]	  
      e = e + (val/len(y[y == i]))
      kk = nump.zeros(k2)
   e = e/k1
   return(e)   

def getSilhouette(x, c, me):
   if VERBOSE:
      print(c)
      print(y)
   
   n = len(c)
   s = nump.zeros((n,3))
   for i in range(n):
      dist = nump.sqrt(nump.sum(nump.power(x[i,:] - me,2), axis=1))
      dd = nump.argsort(dist)
      aa = nump.arange(n)
      for j in range(2):
         aa = nump.arange(n)
         idx = aa[c == dd[j]]
         l = len(idx)
         if l:
            for o in idx:
               s[o,j] = s[o,j] + nump.sqrt(nump.sum(nump.power(x[i,:] - x[o,:] ,2)))
            s[o,j] = s[o,j]/l
   s = nump.mean((s[:,0] - s[:,1])/nump.amax(s[:,0:2], axis=1))
   return(s)

def actionselection(action, probability, numactions, numdims):
   for i in range(numdims):
      a = nump.random.choice(nump.arange(0, numactions), p = probability[:,i])
      mask = nump.zeros(numactions,dtype=bool)
      #print(i, a, mask)
      mask[a] = True
      action[mask,i] = 1
      action[~mask,i] = 0
   return(action)

def probabilityupdate(action, probability, numactions, numdims, signal, alpha, beta):
   if(numactions > 1):
      for i in range(numdims):
         a = nump.where(action[:,i] == 1)
         mask = nump.zeros(numactions,dtype=bool)
         mask[a] = True

         if not signal[i]:
            probability[mask,i] = probability[mask,i] + alpha * (1 - probability[mask,i])
            probability[~mask,i] = (1 - alpha) * probability[~mask,i]
         else:
            probability[mask,i] = (1 - beta) * probability[mask,i]
            probability[~mask,i] = (beta/(numactions-1)) + (1-beta) * probability[~mask,i]		 
   return(probability)

