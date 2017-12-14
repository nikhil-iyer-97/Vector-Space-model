import numpy
import heapq
from math import log,sqrt
from scipy.sparse import csr_matrix
import time

#Class for vectorspacemodel
class VectorSpaceModel():
	
	#Constructor
	def __init__(self):
		self.__words={} #Words is a dict of all words present. Each word is mapped to it's number in the vector
		self.__vectors=None #Vectors is the 2D matrix. Each row is a document's tf-idf vector
		self.__ids=[] #Stores ID's of the documents to be looked up in the database
		self.__wordcount=0 #Number of unique words in the corpus
		self.__doccount=0 #Number of documents in the corpus
		self.__sparsitycount=0 #Number of non-zero entries in the matrix

	def getStats(self):
		return (self.__doccount, self.__wordcount)

	def processDocuments(self,documents): #document is a list of tuples - 1st element contains id, 2nd element contains document as a list of words
		for document in documents:
			for word in document[1]:
				if word not in self.__words:
					self.__words[word]=self.__wordcount
					self.__wordcount+=1

		print(len(documents),self.__wordcount)
		self.__vectors=numpy.zeros((len(documents),self.__wordcount))
		
		for document in documents:
			self.__addDocument(document)

		#idf is an array containing idf of each word
		idf=numpy.zeros((self.__wordcount))
		
		#first calculates df
		for word in self.__words:
			x=self.__words[word]
			for i in range(len(self.__vectors)):
				if self.__vectors[i][x]!=0:
					idf[x]+=1

		#calculates idf of all words as log(n/df)
		for i in range(self.__wordcount):
			idf[i]=log(len(self.__vectors)/idf[i])

		
		#assigns score as (1 + log(tf))*(idf)
		#calculates sparsity count along the way
		for i in range(len(self.__vectors)):
			for j in range(self.__wordcount):
				if self.__vectors[i][j]!=0:
					self.__sparsitycount+=1
					self.__vectors[i][j]=(1+log(self.__vectors[i][j]))*(idf[j])
		
		#Convert each vector to unit vector
		for i in range(len(self.__vectors)):
			l=0
			l=sum(self.__vectors[i]*self.__vectors[i])
			l=sqrt(l)
			if l!=0:
				self.__vectors[i]/=l

		#self.__vectors=csr_matrix(self.__vectors)


	def __addDocument(self,document): #adds document to the vectors
		self.__ids.append(document[0])
		for word in document[1]:
			self.__vectors[self.__doccount][self.__words[word]]+=1
		self.__doccount+=1

	def getSimilarDocuments(self,query,k): #query is a list of words
		vector=numpy.zeros((self.__wordcount))
		for word in query:
			if word in self.__words:
				vector[self.__words[word]]+=1

		for i in range(self.__wordcount):
			if vector[i]!=0:
				vector[i]=1+log(vector[i])

		#The query is now converted to a tf vector
		#And it's cosine similarity is computed
		h=[]
		for i in range(self.__doccount):
			h.append((-1*(self.__calcCosineSimilarity(vector,i)),i))

		#The top k similar documents are obtained using a heap
		heapq.heapify(h)

		ans=[]
		for i in range(k):
			ans.append(heapq.heappop(h))

		return ans

	def __calcCosineSimilarity(self,query,id): #Calculates cosine similarity as the dot product of 2 unit vectors
		return query.dot(self.__vectors[id])
		

def main():
	pass

if __name__=="__main__":
	main()