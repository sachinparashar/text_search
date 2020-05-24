class Trie:
	'''
		Class Trie is works on Trie algorithm which takes sequence of single words and creates tree.
		After creating tree we can search for the given sequence of string.
	'''
	def __init__(self):
		'''
			It creates the first node as {"*":"*"} in the node.
		'''
		self.root = {"*":"*"}

	def add_word(self,text,id):
		'''
			add_word function is used to create a tree structure with the given sequence of words.
			It takes string and after spliting the string, it creates the tree of words.
		'''
		curr_node = self.root
		txt = text.split()

		for t in range(0 , len(txt)):
			if txt[t] not in curr_node:				
				curr_node[txt[t]] = {}

			#if the current node node not contains the word then we create the word as parent's child	
			curr_node = curr_node[txt[t]]

		#if we reaches at the end of the word then it store the string id passed as parameter in to leaf node
		#Looks like {".":"1"}
		curr_node["."] = id

	def count_match(self,summery):
		'''
			count_match method determines that the tree string is there in the passed string or not
			If match found then it increase the counter by 1.
		'''
		summ = summery.split()
		count = 0
		i = 0
		found_query = -1
		curr_node = self.root
		while i<len(summ):	
			
			if summ[i] in curr_node:
				curr_node = curr_node[summ[i]]
				i+=1
			else:
				if "." in curr_node:	
					found_query = curr_node['.']						
					count+=1				

				if curr_node == self.root:
					i+=1
				else:
					curr_node = self.root
				
		if "." in curr_node:
			count+=1
			found_query = curr_node['.']

		return count,found_query