from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize, TreebankWordTokenizer, WordPunctTokenizer
from nltk.stem.porter import *

#Removes stopwords
#Uses a standard list of stopwords provided by NLTK
def remove_stopwords(words):
    english_sw = stopwords.words('english')
    return [word for word in words if word not in english_sw]

#Splits sentence(s) into tokens and removes punctuation marks
def string_tokenize(string):
    #tokenizer = WordPunctTokenizer()
    #This tokenizer splits on spaces and fullstops
    tokenizer=TreebankWordTokenizer()
    tokens = tokenizer.tokenize(string.lower())
    #print(tokens)
    return [token for token in tokens if token.isalpha()]
    
def stemming(words):
	#Porter Stemmer
	lis = []
	stemmer = PorterStemmer()
	for i in range(len(words)):
		lis.append(stemmer.stem(words[i]))
	return lis
'''
4 different approaches to the problem
Depending on the type of corpus/documents, different approaches can be used
In the design document, different approaches have been used and their performaces have been compared
'''
def process_0(sentence):
	return string_tokenize(sentence)

def process_1(sentence):
	return remove_stopwords(string_tokenize(sentence))

def process_2(sentence):
	return stemming(string_tokenize(sentence))

def process_3(sentence):
	return stemming(remove_stopwords(string_tokenize(sentence)))