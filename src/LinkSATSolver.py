#!/usr/local/bin/python

from lp_maker import *
import numpy
from time import time
#import pycallgraph

class Solver:
    def __init__(self):
        pass    

    def f3(self, a, b):
        if a == 0 or b == 0:
            return 0
        else:
            return 1
    
    def solve(self,xlist,X,rX):
        #print xlist
        if len(xlist) == 1:
            if rX[0] > 0:
                X[abs(rX[0])-1] = 1
            elif rX[0] < 0:
                X[abs(rX[0])-1] = 0
            rlist = [1]
            return numpy.array(rlist)
        tlist = [xlist.tolist()]
        xl = []
        for i in xrange(len(rX)):
            xl.append(X[abs(rX[i])-1])
        xln = numpy.array(xl)
        rx = numpy.sum(numpy.extract(numpy.greater(xln,0), xln))# + len(numpy.extract(numpy.equal(xln,0), xln))
        r1 = numpy.sum(numpy.extract(numpy.greater(xlist,0), xlist))        
        r = r1 + numpy.sum(numpy.extract(numpy.less(xlist,0), xlist))                      
        srrx = r+rx        
        if srrx!= 0:        
            tlistr = [srrx]
        else:
            tlistr = [r1+rx]
        eqlist = [0]
        for i in xrange(len(xlist)):
            sX = numpy.zeros(len(xlist),numpy.int)
            sX[i] = 1
            tlist.append(sX.tolist())
            tlistr.append(1)
            eqlist.append(-1)
        for i in xrange(len(xlist)):
            sX = numpy.zeros(len(xlist),numpy.int)
            sX[i] = 1
            tlist.append(sX.tolist())
            tlistr.append(0)
            eqlist.append(1)
        for i in xrange(len(rX)):
            sX = numpy.zeros(len(xlist),numpy.int)
            if X[abs(rX[i])-1] != -1:
                sX[i] = 1
                tlist.append(sX.tolist())
                tlistr.append(X[abs(rX[i])-1])
                eqlist.append(0)
        lp = lp_maker(xlist.tolist(), tlist, tlistr, eqlist, None, None)
        lpsolve('solve', lp)
        rlist = lpsolve('get_variables', lp)[0]
        lpsolve('delete_lp', lp)
        return numpy.array(rlist)
    
    def update(self,clist,rlist,rX,X,it):
        for i in xrange(len(rlist)):
            arXi1 = abs(rX[i]) - 1
            if clist[i] >= 0 and X[arXi1] == -1:
                X[arXi1] = rlist[i]
            elif clist[i] >= 0 and X[arXi1] != -1:
                if X[arXi1] != 1:
                    #X[arXi1] = rlist[i]
                    pass
            elif clist[i] < 0 and X[arXi1] == -1:
                X[arXi1] = 1 - rlist[i]
            elif clist[i] < 0 and X[arXi1] != -1:
                if X[arXi1] != 0:
                    #X[arXi1] = 1 - rlist[i]
                    pass
            else:
                pass             
        return X
    
    def ksat(self,X,filename):
        f = open(filename,'r')
        l = f.readline()
        while l.find('p ')<0:
            l = f.readline()
        ll = l.split(' ')
        nv = int(ll[2])
        nc = int(ll[3])        
        kiek = nc
        kiekX = nv
        rez = 1
        xlist = numpy.zeros(kiekX,numpy.int)
        for i in xrange(kiek):
            line=f.readline()
            if not line: break
            ln = line.split(' ')
            for j in xrange(len(ln)-1):
                rXi = int(ln[j])
                arXi1 = abs(rXi) - 1
                if rXi > 0:
                    xlist[arXi1] = X[arXi1]
                elif rXi < 0:
                    xlist[arXi1] = 1 - X[arXi1]
            rez = self.f3(rez,numpy.sum(xlist))
            #print rez
            if rez == 0: 
                return rez
        return rez

    def readcnfHead(self,filename):
        f = open(filename,'r')
        l = f.readline()
        while l.find('p ')<0:
            l = f.readline()
        ll = l.split(' ')
        desk = ll[0]
        name = ll[1]
        nv = int(ll[2])
        nc = int(ll[3])
        print desk,name, nv, nc
        f.close()
        return nv,nc  
        
    def output(self,rez,X,fout):
        if rez:
            print 'SAT'
            print '[',    
            for i in xrange(len(X)):    
                if X[i] != 0:        
                   if fout=='DIMACS':
                       print i+1,
                   else:
                       print X[i],
                else:
                    if fout=='DIMACS':
                       print -(i+1),
                    else:
                       print X[i],
                if i> 0 and not i%100:
                    print '\n',
            print ']' 
        else:
            print 'UNSAT'
    
if __name__ == '__main__':
    #pycallgraph.start_trace()
    list = []
    s = Solver()
    filename = 'inputaes.cnf'#'aes-10-10-36.cnf'#'inputapp2.cnf'
    N,nn = s.readcnfHead(filename)
    X = numpy.array(  [ -1 for j in xrange(N)]  )
    avksat = []
    tsum = 0
    rez = 1
    it = 0              
    for ci in [1,2,3]:
        f = open(filename,'r')
        l = f.readline()
        while l.find('p ')<0:
            l = f.readline()
        ll = l.split(' ')
        nv = int(ll[2])        
        for k in xrange(nn):           
            t0 = time()
            line=f.readline()
            if not line: break
            ln = line.split(' ')
            if ci == 1:            
                if len(ln)>2: continue
            elif ci == 2:
                if len(ln)!=3: continue
            elif ci == 3:
                if len(ln)<=3: continue
            clist = []
            rX = []
            for i in xrange(len(ln)-1):
                rXi = int(ln[i])
                rX.append(rXi)
                if rXi>0: 
                    clist.append(1)
                elif rXi<0:
                    clist.append(-1)
            avksat.append(len(clist))
            rlist = s.solve(numpy.array(clist,numpy.int),X,rX)
            print 'iter ',k+1,'rlist ',rlist
            X = s.update(clist,rlist,rX,X,it)
            t1 = time()
            tsum += t1 - t0
            it += 1          
        f.close() 
    rez = s.ksat(X,filename)
    print "%d; %f; %d; %d"%(nn,tsum,rez,max(avksat))
    s.output(rez,X,'BINARY')#BINARY & DIMACS
    numpy.delete(X,X,None)
    #pycallgraph.make_dot_graph('test.png')
        
