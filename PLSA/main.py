
# imports from python std lib
from math import log10

STOPWORDS = ["is", "and", "of", "are", "a", "an", "the", "for", "that", "do", "to", "in", ]
PUNCTUATIONS = [".", ",", ";", ":"]

def log(n):
	if n == 0:
		return 0
	return log10(n)

class LSI:
	def __init__(self, dataset, K=10, maxIteration=30, threshold=10):
		self.K = K    # number of topic
		self.maxIteration = maxIteration
		self.threshold = threshold

		# prepareData
		self.id2word, self.word2id, self.N, self.corpus = self.prepareData(dataset)

		# number of unique words
		self.M = len(self.id2word)

		# construct the A matrix
		self.A = self.constructMatrix(self.corpus)

		# display the A matrix
		self.displayMatrix()
		
		# DT[i, j] : p(zj|di)
		self.DT = self.constructMatrix('random', self.N, self.K)

		# TW[i, j] : p(wj|zi)
		self.TW = self.constructMatrix('random', self.K, self.M)

		# T[i, j, k] : p(zk|di,wj)
		self.T = [[[randint(0, 100) for k in range(K)] for j in range(M)] for i in range(N)]

		# normalizes DT and TW
		initializeParameters()

		# EM algorithm
		oldLoglikelihood = 1
		newLoglikelihood = 1
		for i in range(0, maxIteration):
			# run EM
		    self.EStep()
		    self.MStep()
		    
		    newLoglikelihood = self.LogLikelihood()
		    
		    print("[", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), "] ", i+1, " iteration  ", str(newLoglikelihood))
		    if(oldLoglikelihood != 1 and newLoglikelihood - oldLoglikelihood < threshold):
		        break
		        
		    oldLoglikelihood = newLoglikelihood

	def constructMatrix(self, fromMatrix, N=None, M=None):
		'''
		constructs the A matrix
		N - number of documents
		M - number of unique words

		fromMatrix is a list of list that contain list of words in document for each document
		'''
		if N == None:
			N = self.N

		if M == None:
			M = self.M
		
		A = []
		for i in range(N):
			row = []
			for j in range(M):
				n = 0
				
				# if word_id in document j
				if type(fromMatrix) == list and j in fromMatrix[i]:
					n = fromMatrix[i].count(j)

				if fromMatrix == 'random':
					n = randint(0, 100)
				
				row.append(n)

			A.append(row)
		return A

	def displayMatrix(self, A=None):
		'''
		A is a M by N matrix
		'''
		if A==None:
			A = self.A

		for row in A:
			print(" ".join([format(x, "5.2f") for x in row]))
		print()

	def initializeParameters(self, TW=None, DT=None):
		if TW == None:
			TW = self.TW

		if DT == None:
			DT = self.DT

		N, M, K = len(DT), len(TW[0]), len(TW)
	    for i in range(0, N):
	        normalization = sum(DT[i])
	        for j in range(0, K):
	            DT[i][j] /= normalization;

	    for i in range(0, K):
	        normalization = sum(TW[i])
	        for j in range(0, M):
	            TW[i][j] /= normalization;

	def EStep(self, TW=None, DT=None, DW=None, T=None):
		if TW == None:
			TW = self.TW

		if DT == None:
			DT = self.DT

		if DW == None:
			DW = self.DW

		if T == None:
			T = self.T
			
		N, M, K = len(DW), len(DW[0]), len(TW)
	    for i in range(0, N):
	        for j in range(0, M):
	            denominator = 0;
	            for k in range(0, K):
	                T[i][j][k] = TW[k][j] * DT[i][k];
	                denominator += T[i][j][k];
	            if denominator == 0:
	                for k in range(0, K):
	                    T[i][j][k] = 0;
	            else:
	                for k in range(0, K):
	                    T[i][j][k] /= denominator;

	def MStep(self, TW=None, DT=None, DW=None, T=None):
		if TW == None:
			TW = self.TW

		if DT == None:
			DT = self.DT

		if DW == None:
			DW = self.DW

		if T == None:
			T = self.T

		N, M, K = len(DW), len(DW[0]), len(TW)
	    # update TW
	    for k in range(0, K):
	        denominator = 0
	        for j in range(0, M):
	            TW[k][j] = 0
	            for i in range(0, N):
	                TW[k][j] += DW[i][j] * T[i][j][k]
	            denominator += TW[k][j]
	        if denominator == 0:
	            for j in range(0, M):
	                TW[k][j] = 1.0 / M
	        else:
	            for j in range(0, M):
	                TW[k][j] /= denominator
	        
	    # update DT
	    for i in range(0, N):
	        for k in range(0, K):
	            DT[i][k] = 0
	            denominator = 0
	            for j in range(0, M):
	                DT[i][k] += DW[i][j] * T[i][j][k]
	                denominator += DW[i][j];
	            if denominator == 0:
	                DT[i][k] = 1.0 / K
	            else:
	                DT[i][k] /= denominator

	# calculate the log likelihood
	def LogLikelihood(self, TW=None, DT=None, DW=None):
		if TW == None:
			TW = self.TW

		if DT == None:
			DT = self.DT

		if DW == None:
			DW = self.DW

		N, M, K = len(DW), len(DW[0]), len(TW)
	    loglikelihood = 0
	    for i in range(0, N):
	        for j in range(0, M):
	            tmp = 0
	            for k in range(0, K):
	                tmp += TW[k][j] * DT[i][k]
	            if tmp > 0:
	                loglikelihood += DW[i][j] * log(tmp)
	    return loglikelihood

	def prepareData(self, dataset):
		'''
		converts the dataset to usable data for LSI
		'''

		documents = dataset
		
		# holds the last index assigned
		index = 0

		# holds the vocabulary with the unique word as key
		word2id = {}

		# holds the vocabulary with the id the key to the word
		id2word = {}

		# number of documents
		N = len(documents)

		corpus = [] #Document words
		# loop through the entire corpus
		for document in documents:
			# list containing words in the document
			words_in_document = []

			words = document.split(" ")
			for wordx in words:
				word = wordx.lower()

				if word[-1] in PUNCTUATIONS:
					word = word[:-1]

				if word in STOPWORDS or word in PUNCTUATIONS:
					continue

				if word not in word2id:
					word2id[word] = index
					id2word[index] = word
					index += 1 #update the index to be assigned to another unique word

				words_in_document.append(word2id[word])
			corpus.append(words_in_document)
		return id2word, word2id, N, corpus

if __name__ == '__main__':
	dataset = [
		"Romeo Juliet.",
		"Juliet happy dagger!",
		"Romeo die dagger.",
		"Live free die New-Hampshire",
		"New-Hampshire"
	]
	LSIObject = LSI(dataset)