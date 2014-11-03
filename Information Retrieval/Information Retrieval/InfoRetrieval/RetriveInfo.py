'''
Created on Nov 2, 2014

@authors: downinew
          Haydr
'''
import os
import math
from cgi import log

def main():
    BM25 = [("noname",100)]
    PhaseExtensionTopTen = []
    NGRAM = []
    array = ["franklin"]
    
    rootDir = 'Presidents'
    for dirPath, dirNames, fileNames in os.walk(rootDir):
        for file in fileNames:
            f = open('Presidents/' + file,'r')
            D = f.read().lower().split()
            bm25Score = BM25ScoringFunction(D, array)
            nGramScore = nGram(D, array)
            NGRAM.insert(0, (nGramScore,file))
            BM25.insert(0, (bm25Score,file))
            f.close()
            
    BM25.sort()
    NGRAM.sort(cmp=None, key=None, reverse=True)
    NGRAM = Top10(NGRAM)
    BM25 = Top10(BM25)
    print(BM25)
    print(NGRAM)
        
def BM25ScoringFunction(D, Q):
    score = 0
    qiInD = 0
    avgdl = avGDL()
    for Qi in Q:
        IDF = IDFNumber(Qi)
        for word in D:
            if word == Qi:
                qiInD += 1
        score += IDF * ((qiInD + 2.2) / (qiInD + 1.2 * (1-.75 + .75 * (len(D)/avgdl))))
    return score
        
        
        
def IDFNumber(query):
    count = 0
    rootDir = 'Presidents'
    for dirPath, dirNames, fileNames in os.walk(rootDir):
        for file in fileNames:
            f = open('Presidents/' + file,'r')
            contents = f.read().lower().split()
            for word in contents:
                if word == query:
                    count += 1
            f.close()
    top = (43 - count + .5)
    bottom = (count + .5)
    number = top / bottom
    if number < 0:
        number = number + 10
    IDFscore = math.log(number)
    return IDFscore

def avGDL():
    totalLength = 0
    count = 0
    rootDir = 'Presidents'
    for dirPath, dirNames, fileNames in os.walk(rootDir):
        for file in fileNames:
            f = open('Presidents/' + file,'r')
            contents = f.read().split()
            totalLength += len(contents)
            count += 1
            f.close()
    avgld = totalLength / count
    return avgld

def Top10(topTenArray):
    newArray = []
    for i in range(10):
        newArray.append(topTenArray[i])
    topTenArray = newArray
    return topTenArray


def nGram(D,array):
    n = len(array)
    index = 0
    count = 0
    nGramCheck = 0
    while(index + n <= len(D)):
        for query in array:
            for i in range(index, index+n):
                if D[i] == query:
                    count += 1
        if count % n == 0:
            nGramCheck += 1
        index += 1
    return nGramCheck
                
    
    




if __name__ == '__main__':
    main()