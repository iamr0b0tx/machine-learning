
STOPWORDS = ["is", "and", "of", "are", "a", "an", "the"]
PUNCTUATIONS = [".", ",", ";", ":"]

class LSI:
	def __init__(self, dataset):
		# get the vocabulary and the document count
		self.id2word, self.word2id, self.N = self.prepareData(dataset)
		
		# number of unique words
		self.M = len(self.id2word)

		# construct the A matrix
		self.A = self.constructMatrix()

		#set the weights on the matrix A
		self.A = self.localGlobalWeight()

	def constructMatrix(self, N=None, M=None):
		'''
		constructs the A matrix
		N - number of documents
		M - number of unique words
		'''
		if N == None:
			N = self.N

		if M == None:
			M = self.M
		return [[0 for j in range(N)] for i in range(M)]

	def localGlobalWeight(self, A=None):
		if A == None:
			A = self.A

		for row in A:
			for element in row:
				print(element, end="")
		return self.logEntropy()

	def logEntropy(self):
		pass

	def prepareData(self, dataset):
		documents = dataset
		# holds the last index assigned
		index = 0

		# holds the vocabulary with the unique word as key
		word2id = {}

		# holds the vocabulary with the id the key to the word
		id2word = {}

		N = len(documents)

		# loop through the entire corpus
		for document in documents:
			words = document.split(" ")
			for word in words:
				if word in STOPWORDS or word in PUNCTUATIONS:
					continue

				if word not in word2id:
					word2id[word] = index
					id2word[index] = word
					index += 1 #update the index to be assigned to another unique word
		return id2word, word2id, N

if __name__ == '__main__':
	dataset = [
		"what is teh way home",
		"can i see the way to the market please",
		"jump the map to the can",
	]
	LSIObject = LSI(dataset)