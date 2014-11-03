'''
Created on Nov 2, 2014

@authors: downinew
          Haydr
'''
import os
import math
from cgi import log
from string import lowercase
from audioop import reverse

def main():
    BM25 = [("noname",100)]
    textAlign = []
    NGRAM = []
    array = ["assassinated","president"]
    
    rootDir = 'Presidents'
    for dirPath, dirNames, fileNames in os.walk(rootDir):
        for file in fileNames:
            f = open('Presidents/' + file,'r')
            D = f.read().lower().split()
            bm25Score = BM25ScoringFunction(D, array)
            nGramScore = nGram(D, array, 5)
            textAlignScore = TextualAlignment(D, array)
            if textAlignScore > 0:
                textAlign.insert(0, (textAlignScore,file))
            if nGramScore > 0:
                NGRAM.insert(0, (nGramScore,file))
            BM25.insert(0, (bm25Score,file))
            f.close()
    textAlign.sort(reverse=True)
    BM25.sort()
    NGRAM.sort(cmp=None, key=None, reverse=True)
    BM25 = Top10(BM25)
    if len(NGRAM) > 10:
        NGRAM = Top10(NGRAM)
    if len(textAlign) > 10:
        textAlign = Top10(textAlign)
    print(BM25)
    print(NGRAM)
    print(textAlign)
        
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
            contents = f.read().split()
            for word in contents:
                if word == query:
                    count += 1
            f.close()
    top = (43 - count + .5)
    bottom = (count + .5)
    number = top / bottom
    if(number< 0):
        number += 10
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


def nGram(D,array,n):
    index = 0
    nGramCheck = 0
    while(index + n <= len(D)):
        count = 0
        for query in array:
            for i in range(index, index+n):
                if D[i] == query:
                    count += 1
        if count == len(array):
            nGramCheck += 1
        index += 1
    return nGramCheck

def TextualAlignment(D, array):
    index = 0
    textCheck = len(array)
    score = 0
    while(index + textCheck <= len(D)):
        matches = 0
        for i in range(index, index + textCheck):
            for query in array:
                if D[i] == query:
                    matches += 1
        score += matches * .75
        index += 1
    return score


if __name__ == '__main__':
    main()