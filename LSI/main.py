
# imports from python std lib
from math import log10

STOPWORDS = ["is", "and", "of", "are", "a", "an", "the", "for", "that", "do", "to", "in", ]
PUNCTUATIONS = [".", ",", ";", ":"]

def log(n):
	if n == 0:
		return 0
	return log10(n)

class LSI:
	def __init__(self, dataset):
		# get the vocabulary and the document count
		self.id2word, self.word2id, self.N, words_in_documents = self.prepareData(dataset)
		
		# number of unique words
		self.M = len(self.id2word)

		# construct the A matrix
		self.A = self.constructMatrix(words_in_documents)

		# display the A matrix
		self.displayMatrix()

		#set the weights on the matrix A
		# self.A = self.localGlobalWeight()

		# display the A matrix
		self.displayMatrix()

		#svd
		self.U, self.S, self.V = self.SVD()

	def constructMatrix(self, words_in_documents, N=None, M=None):
		'''
		constructs the A matrix
		N - number of documents
		M - number of unique words

		words_in_documents is a list of list that contain list of words in document for each document
		'''
		if N == None:
			N = self.N

		if M == None:
			M = self.M
		
		A = []
		for i in range(M):
			row = []
			for j in range(N):
				n = 0
				
				# if word_id in document j
				if i in words_in_documents[j]:
					n = words_in_documents[j].count(i)
				
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

	def getMatrixSize(self, A):
		'''
		A is a matrix
		returns the row number and column number
		'''
		if len(A) == 0:
			return 0, 0

		return len(A), len(A[0])

	def localGlobalWeight(self, A=None):
		'''
		A is a M by N matrix holding the frequency of words in documents
		the local weighting function used is Log
		and the global weight function used is Entropy
		'''
		if A == None:
			A = self.A

		return self.logEntropy(A)

	def logEntropy(self, A):
		document_RHS_sum = []

		# number of unique words
		M = len(A)

		for i in range(M):
			row = A[i]

			# number of documents
			N = len(row)

			document_RHS = []
			for j in range(N):
				# number of times i appears in the whole corpus
				gf_i = sum(row)

				#number of times i appears in the document
				tf_ij = A[i][j]

				p_ij = tf_ij/gf_i

				# for the g_i function
				RHS = (p_ij * log(p_ij))/log(N)
				document_RHS.append(RHS)
			document_RHS_sum.append(sum(document_RHS))

		for i in range(M):
			for j in range(N):
				tf_ij = A[i][j]
				g_i = 1 + document_RHS_sum[j]
				A[i][j] = g_i * log(tf_ij + 1)
		return A

	def matrixMultiplication(self, X, Y):
		X_R, X_C = self.getMatrixSize(X)
		Y_R, Y_C = self.getMatrixSize(Y)

		if X_C != Y_R:
			raise("Error: Inavlid Matrix Multiplication")

		product = []
		for r in range(X_R):
			product.append([])
		
			for j in range(Y_C):
				new_element = 0

				for i in range(X_C):
					new_element += X[r][i] * Y[i][j]

				product[r].append(new_element)
		return product

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

		words_in_documents = []
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
			words_in_documents.append(words_in_document)
		return id2word, word2id, N, words_in_documents

	def tranposeMatrix(self, A):
		R, C = self.getMatrixSize(A)
		return [[A[r][c] for r in range(R)] for c in range(C)]
		
	def SVD(self, A=None):
		if A == None:
			A = self.A

		# get singular values
		A_transposed = self.tranposeMatrix(A)

		self.displayMatrix(A_transposed)

		# U = self.matrixMultiplication(A, A_transposed)
		U = self.matrixMultiplication(A_transposed, A)
		self.displayMatrix(U)

		U, S, V = 0,0,0
		return U, S, V
if __name__ == '__main__':
	dataset = [
		"Romeo Juliet.",
		"Juliet happy dagger!",
		"Romeo die dagger.",
		"Live free die New-Hampshire",
		"New-Hampshire"
	]
	LSIObject = LSI(dataset)