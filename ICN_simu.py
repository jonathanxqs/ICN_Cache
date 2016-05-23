#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import copy
import sys

#import cache_replace.CLOCK
#print(cache_replace.CLOCK)
import random
import cache_replace

#from cache_replace import *


__author__="Jonathan Xu"

  ##  Global var-----------------

ipNodeDict=dict()
nodeIpDict=dict()
fileHandlerGraph="Topology_Graph.txt"
fileHandleName="Tencent_req_data1.txt"

replaceAlg=cache_replace.LRU  #LRU,LFU
replaceCacheSize = 12     # >= 1
placeAlg='LCE'
p = 0.2          # Prob

N_max=202
reqN=0
linkStatus=[[0 for i in range(N_max)] for j in range(N_max)]


path=[[]]        #Floyd 

hitTimesTotal=0;
checkTimesTotal=0;
hitRatio=0
hitTimeVec = [0 for i in range(N_max)]
sumLength1 = 0



nodeAlgVec=[] #node alg vector

dis1=1
n=0 #node total number


#ip -> node number
def Nodify(ip_add):
    global nodeIpDict

    if  nodeIpDict.get(ip_add) != None:
        return nodeIpDict[ip_add] 
    else:
        return None


# #------------------initialization

def initSet():

    

    print("N_max=",N_max)
    #print(linkStatus)

    global path
    global nodeAlgVec
    global ipNodeDict,nodeIpDict
    
    path=copy.deepcopy(linkStatus)
    

    with open(fileHandlerGraph, 'r') as f:
        i=0
        global n
        n=int(f.readline())
        print(n)

        while i<n:
            line=f.readline()
            lineArr=line.split()
            ip1=lineArr[1]
            node1=int(lineArr[0])

            #print(ip1,node1)

            ipNodeDict[node1] = ip1
            nodeIpDict[ip1] = node1

            nodeAlgVec.append(replaceAlg.alg(replaceCacheSize,i))
            i += 1
            
        #print(ipNodeDict[0])
        print("LRU numbers:",len(nodeAlgVec))

        for line in f.readlines():                      
            #print(line)

            lineArr=line.strip().split()
            #print(lineArr)


            if len(lineArr)     >2 : 
                dis1=lineArr[2] 
            else: 
                dis1=1          

            #print(lineArr[0],nodeIpDict[lineArr[0]])
            print(Nodify(lineArr[0]),Nodify(lineArr[1]),dis1)
                   

            linkStatus[Nodify(lineArr[0])][Nodify(lineArr[1])] = dis1
            linkStatus[Nodify(lineArr[1])][Nodify(lineArr[0])] = dis1

    print("Set up the Topology_Graph successfully!")
    print("In init n=",n)

   
    


def floydInit():

    N = n
    print("n=",n,"N=",N)
    _maxInf=float('inf')      #无穷大
    print(_maxInf)
    global linkStatus
    graph=copy.deepcopy(linkStatus)

    for i in range(n):
        for j in range(n):
            if not linkStatus[i][j]:
                graph[i][j]=_maxInf

    for i in range(n):
        graph[i][i]=0

    #print(path)
    for i in range(n):
        for j in range(n):
            path[i][j] = -1
    
    #print(path)    
    #print("Graph:\n",graph)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if graph[i][j] > graph[i][k] + graph[k][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]
                    path[i][j] = k
                    
    #print("Shortest distance:\n",graph)
    #print("Path:\n",path)
    #print("Points pass-by:")
    #for i in range(n):
    #    for j in range(n):
    #        print("%d -> %d:" % (i,j))
    #        print(findPath(i,j))
            
    print("Init flyod successfully")
    return 

def back_path(path,i,j,t):

        while(-1 != path[i][j]):
            back_path(path,i,path[i][j],t)
            back_path(path,path[i][j],j,t)
            #print(path[i][j],)
            t.append(path[i][j])
            return;
        return
    

def findPath(node_source,node_dest):
    s=[]
    back_path(path,node_source,node_dest,s)
    return s

def LCEExe(reqFileName,node_source,node_dest):

    global hitTimeVec,hitTimesTotal,sumLength1

    path1=findPath(node_source,node_dest)
    if not node_dest in path1:
        path1.append(node_dest)
    if not node_source in path1:
        path1.insert(0,node_source)
    len1=len(path1)
    #print(len1)
    sumLength1 += len1

    for i in range(len1):
        if nodeAlgVec[path1[i]].get(reqFileName):
            #print("L = Source user,R = Dest server,Find the reqFile in:",ipNodeDict[path1[i]],"Naming and Acutal Req Length=",len(path1),i+1)
            if  i<len1-1 : 
                hitTimeVec[i] += 1
                hitTimesTotal += 1
                sumLength1 += ((1+i) -len1)
                #nodeAlgVec[path1[i]].walk()

            for j in range(0,i+1):
                #print("i,j=",i,j,"To:",path1[i],"At:",path1[j])
                nodeAlgVec[path1[j]].put(reqFileName)
                #nodeAlgVec[path1[j]].walk()

            break
        else:
            pass


        #cache_replace.sim


def LCDExe(reqFileName,node_source,node_dest):

    global hitTimeVec,hitTimesTotal,sumLength1
    path1=findPath(node_source,node_dest)
    

    if not node_dest in path1:
        path1.append(node_dest)
    if not node_source in path1:
        path1.insert(0,node_source)

    len1=len(path1)
    #print(len1)

    sumLength1 += len1

    for i in range(len(path1)):
        if (nodeAlgVec[path1[i]].get(reqFileName)):
            if i<len1-1:

                    hitTimeVec[i] += 1
                    hitTimesTotal += 1
                    sumLength1 += ((1+i) -len1)

            if i>0:
                nodeAlgVec[path1[i-1]].put(reqFileName)                

            break

        
def ProbExe(reqFileName,node_source,node_dest):

    
    
    global hitTimeVec,hitTimesTotal,sumLength1
    path1=findPath(node_source,node_dest)
    

    if not node_dest in path1:
        path1.append(node_dest)
    if not node_source in path1:
        path1.insert(0,node_source)

    len1=len(path1)
    #print(len1)

    sumLength1 += len1

    for i in range(len(path1)):
        
        if (nodeAlgVec[path1[i]].get(reqFileName)):
            if i<len1-1:

                    hitTimeVec[i] += 1
                    hitTimesTotal += 1
                    sumLength1 += ((1+i) -len1)                                                         

            break

        
        j = random.random()
        if j>p:
            nodeAlgVec[path1[i]].put(reqFileName) 




#request Execute
def reqExe(reqFileName,node_source,node_dest,placeAlg,**kargs):

    
    if placeAlg == 'LCE':
        LCEExe(reqFileName,node_source,node_dest)
 
    elif placeAlg =='LCD':
        LCDExe(reqFileName,node_source,node_dest)

    elif  placeAlg.upper()  =='PROB':                
        ProbExe(reqFileName,node_source,node_dest)
    
    else:
        print("No such algorithm")




#request import all
def reqImport(fileHandle1,placeAlg):

    global nodeAlgVec,reqN
    

    with open(fileHandle1, 'r') as f:
        for line in f.readlines():
            
            words=line.split()
            if not words:
                continue


            if reqN %50000 ==0:
                print("reqN and time = ",reqN,time.time())
            reqN += 1
            #print(words)
            
            ip_source=words[0]
            ip_dest=words[1]
            reqFileName=words[2]
            node_source=Nodify(ip_source)
            node_dest=Nodify(ip_dest)
            #print(ip_source,node_source)
            #print(ip_dest,node_dest)
            
            nodeAlgVec[node_dest].put(reqFileName)
            #nodeAlgVec[node_dest].walk()
            reqExe(reqFileName,node_source,node_dest,placeAlg)
            

        print("req all import successfully!")

def statPrint():

    global hitTimesTotal,checkTimesTotal,hitRatio,reqN
    
    if reqN %50000 ==0:
        print("reqN and time = ",reqN,time.time())
    #for i in range(n):
    #            hitTimesTotal += nodeAlgVec[i].hitcount
    #            checkTimesTotal += nodeAlgVec[i].count

    print("Hit times Total  =",hitTimesTotal)
    print("ReqTimesTotal  =", reqN)
    print("Hit Ratio=",hitTimesTotal/reqN)

    global sum 
    for i in range(N_max):
        if hitTimeVec[i] == 0 and hitTimeVec[i+1] == 0:
            break
        else:
            pass
        print("Hit times in the level",i,"is :",hitTimeVec[i]," ratio:",hitTimeVec[i]/reqN)

    print("The average length of get:",sumLength1 / reqN)
    print("Stat End Successfully!")
        



#Main program start form here


if __name__ == "__main__":
    print('Start from main')
    initSet()
    
    floydInit()
    reqImport(fileHandleName,placeAlg)
    statPrint()










