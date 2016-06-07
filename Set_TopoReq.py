#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import copy
import sys
import random
import math
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import numpy as np
#import numpy.random.zipf as Dzipf
#import scipy.special as sps


fileHandlerGraph="Topology_Graph.txt"
fileHandleName="Tencent_req_data1.txt"
fileZipf="Zipf_list.txt"
fp = open(fileHandlerGraph,"w+")  


topoNodeMaxn = 1        # 150
requestMaxn = 100000    # 200000
fileMaxn = 3000       # 3000
mBA = 1               # 150 -> 3


nodeVec=[]
ipNodeDict=dict()
nodeIpDict=dict()

sumZipf=[0 for i in range(fileMaxn)]

linkStatus=[[0 for i in range(topoNodeMaxn+1)] for j in range(topoNodeMaxn+1)]

#Random IP dict

def randomIP():
    t=""
    for i in range(3):
        f=random.randint(1,255)
        t+=str(f)
        t+='.'
    f=random.randint(1,255)
    t+=str(f)
    return t


i=0
while i < topoNodeMaxn + 1:
    t=randomIP()
    
    if not t in nodeVec:
        ipNodeDict[t]=i
        nodeIpDict[i]=t
        i += 1
        nodeVec.append(t)
        




#G = nx.random_graphs.barabasi_albert_graph(topoNodeMaxn,mBA)   #generally 200,4  BA
G= nx.random_graphs.random_regular_graph(1,2) 
#G= nx.Graph()
#G.add_node(1)


#print(G.degree(0))                                 
print(G.degree())                                
print(nx.degree_histogram(G))    

# spring layout
pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels = True, node_size = topoNodeMaxn)
plt.show()


fp.write(G.number_of_nodes().__str__()+"\n")
n=G.number_of_nodes()


for i in G.nodes():
    G.node[i]['ipAdd'] = nodeIpDict[i]
    #print(i,G.node[i]['ipAdd'])
    fp.write(str(i)+" "+str(G.node[i]['ipAdd'])+"\n")


    
for i,j in G.edges():
    #print(nodeIpDict[i],nodeIpDict[j])
    fp.write(str(nodeIpDict[i])+" "+str(nodeIpDict[j])+"\n")
    

#print(G.edges())
#print(G.nodes())

fp.close()



#simulate Tencent Req Data

fp=open(fileHandleName,'w+')

def randOp():
    for i in range(requestMaxn):
        j= random.randint(0,n-1)
        k= random.randint(0,n-1)
        while k==j:
            k = random.randint(0,n-1)

        num1= random.randint(0,fileMaxn)
        fp.write(nodeIpDict[j]+" "+nodeIpDict[k]+" "+str(num1)+"\n")


def zipfWrite():
    global sumZipf
    fzipw=open(fileZipf,'w+')
    a = 2.6
    print("a and N =",a,fileMaxn)
    s = np.random.zipf(a, fileMaxn)
    s.sort()
    #s.reverse()

    sc=""
    for i in range(fileMaxn):
        sc += str(s[i])
        sc += " "

    fzipw.write(sc)   
    

    for i in range(fileMaxn):
        if i==0:
            sumZipf[i] = s[i]
            continue

        sumZipf[i] = sumZipf[i-1] + s[i]

    print((sumZipf[fileMaxn-1]-sumZipf[math.floor(4*(fileMaxn)/5)]),sumZipf[fileMaxn-1])
    print("The 20% top sum / total ratio: ",(sumZipf[fileMaxn-1]-sumZipf[math.floor(4*(fileMaxn)/5)])/sumZipf[fileMaxn-1])      
    fzipw.close()


def zipfOp():

    fzipw=open(fileZipf,'r+')
    s1=fzipw.readline()
    s3=s1.split()
    s2=[0 for i in range(fileMaxn)]
    for i in range(fileMaxn):
        s2[i] = int(s3[i])

    #print(s2)
    #print(len(s2))
    sumZipf[0]=s2[0]
    for i in range(1,fileMaxn):
        sumZipf[i] = sumZipf[i-1] + s2[i]
    #print(sumZipf)


    for i in range(requestMaxn):
        #j= random.randint(0,n-1)
        #k= random.randint(0,n-1)
        j=0
        k=1
        while k==j:
            k = random.randint(0,n-1)

        num1= numRandlize()
        fp.write(nodeIpDict[j]+" "+nodeIpDict[k]+" "+str(num1)+"\n")

def numRandlize():
    i = random.randint(0,sumZipf[fileMaxn-1])
    l=0
    r=fileMaxn-1
    #print(i)

    while r >= l:
        mid = math.floor((l+r)/ 2)
        #print(l,r,mid)
        if sumZipf[mid] == i:
            return mid
        if sumZipf[mid] < i:
            
            l = mid + 1
            
        else:
            r = mid - 1
    
    return max(l,r)
        

#randOp()
zipfOp()
#zipfWrite()
    

fp.close()

                    
        
    



