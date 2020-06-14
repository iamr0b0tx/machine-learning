import sys
import jieba
import re
import time
import codecs

# segmentation, stopwords filtering and document-word matrix generating
# [return]:
# N : number of documents
# M : length of dictionary
# word2id : a map mapping terms to their corresponding ids
# id2word : a map mapping ids to terms
# X : document-word matrix, N*M, each line is the number of terms that show up in the document
def prepareData(datasetFilePath, stopwordsFilePath):
    
    # read the stopwords file
    file = codecs.open(stopwordsFilePath, 'r', 'utf-8')
    stopwords = [line.strip() for line in file] 
    file.close()
    
    # read the documents
    file = codecs.open(datasetFilePath, 'r', 'utf-8')
    documents = [document.strip() for document in file] 
    file.close()

    # number of documents
    N = len(documents)

    wordCounts = [];
    word2id = {}
    id2word = {}
    currentId = 0;
    # generate the word2id and id2word maps and count the number of times of words showing up in documents
    for document in documents:
        segList = jieba.cut(document)
        wordCount = {}
        for word in segList:
            word = word.lower().strip()
            if len(word) > 1 and not re.search('[0-9]', word) and word not in stopwords:               
                if word not in word2id.keys():
                    word2id[word] = currentId;
                    id2word[currentId] = word;
                    currentId += 1;
                if word in wordCount:
                    wordCount[word] += 1
                else:
                    wordCount[word] = 1
        wordCounts.append(wordCount);
    
    # length of dictionary
    M = len(word2id)  

    # generate the document-word matrix
    X = zeros([N, M], int8)
    for word in word2id.keys():
        j = word2id[word]
        for i in range(0, N):
            if word in wordCounts[i]:
                DW[i, j] = wordCounts[i][word];    

    return N, M, word2id, id2word, X

def initializeParameters():
    for i in range(0, N):
        normalization = sum(DT[i, :])
        for j in range(0, K):
            DT[i, j] /= normalization;

    for i in range(0, K):
        normalization = sum(TW[i, :])
        for j in range(0, M):
            TW[i, j] /= normalization;

def EStep():
    for i in range(0, N):
        for j in range(0, M):
            denominator = 0;
            for k in range(0, K):
                T[i, j, k] = TW[k, j] * DT[i, k];
                denominator += T[i, j, k];
            if denominator == 0:
                for k in range(0, K):
                    T[i, j, k] = 0;
            else:
                for k in range(0, K):
                    T[i, j, k] /= denominator;

def MStep():
    # update TW
    for k in range(0, K):
        denominator = 0
        for j in range(0, M):
            TW[k, j] = 0
            for i in range(0, N):
                TW[k, j] += DW[i, j] * T[i, j, k]
            denominator += TW[k, j]
        if denominator == 0:
            for j in range(0, M):
                TW[k, j] = 1.0 / M
        else:
            for j in range(0, M):
                TW[k, j] /= denominator
        
    # update DT
    for i in range(0, N):
        for k in range(0, K):
            DT[i, k] = 0
            denominator = 0
            for j in range(0, M):
                DT[i, k] += DW[i, j] * T[i, j, k]
                denominator += DW[i, j];
            if denominator == 0:
                DT[i, k] = 1.0 / K
            else:
                DT[i, k] /= denominator

# calculate the log likelihood
def LogLikelihood():
    loglikelihood = 0
    for i in range(0, N):
        for j in range(0, M):
            tmp = 0
            for k in range(0, K):
                tmp += TW[k, j] * DT[i, k]
            if tmp > 0:
                loglikelihood += DW[i, j] * log(tmp)
    return loglikelihood

    
# set the default params and read the params from cmd
datasetFilePath = 'dataset.txt'
stopwordsFilePath = 'stopwords.dic'
K = 10    # number of topic
maxIteration = 30
threshold = 10.0

# prepareData
N, M, word2id, id2word, DW = prepareData(datasetFilePath, stopwordsFilePath)

# DT[i, j] : p(zj|di)
DT = [[randint(100) for k in range(K)] for i in range(N)]

# TW[i, j] : p(wj|zi)
TW = [[randint(100) for j in range(M)] for k in range(K)]

# T[i, j, k] : p(zk|di,wj)
T = [[[randint(100) for k in range(K)] for j in range(M)] for i in range(N)]

initializeParameters()

# EM algorithm
oldLoglikelihood = 1
newLoglikelihood = 1
for i in range(0, maxIteration):
    EStep()
    MStep()
    newLoglikelihood = LogLikelihood()
    print("[", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), "] ", i+1, " iteration  ", str(newLoglikelihood))
    if(oldLoglikelihood != 1 and newLoglikelihood - oldLoglikelihood < threshold):
        break
    oldLoglikelihood = newLoglikelihood
