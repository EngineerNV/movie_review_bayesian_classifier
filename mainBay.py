#!/usr/bin/env python
from cleanData import remove_format
import string
freshName = "example_fresh.txt"
rottenName = "example_rotten.txt"
test_name = "test_ex_rotten.txt" 
decimal_shift = 100000 # this will mulitply the decimals that are formed for the probability 

class fresh_count: 
	def __init__(self, fresh, rot): 		  
		self.dic_fresh = dict()
		self.dic_rot = dict()
		self.dic_fresh_prob = dict()
		self.dic_rot_prob = dict() 
		self.total_words = 0  
		self.total_rot = 0
		self.total_fresh = 0
		self.fresh_file_name = fresh #these are the file names to the training data 
		self.rot_file_name = rot
		self.result_fresh = 0 
		self.result_rot = 0
		self.f_r_prob = []	
	def read_to_fresh_dic(self): #this will store every single word from the fresh review test file and count how many instances of each one
		dic = self.dic_fresh
		remove_format(self.fresh_file_name)
		f = open(self.fresh_file_name,"r")
		for line in f:
			words = line.split(" ")
			while "\n" in words: words.remove("\n")
			for word in words:
				self.total_fresh += 1
				self.total_words += 1
				if word in dic:
					dic[word] += 1
				else:
					dic[word] = 1				 
	def read_to_rot_dic(self): #this will store every single word from the rotten review test file and count how many instances of each one
		dic = self.dic_rot
		remove_format(self.rot_file_name)
		f = open(self.rot_file_name,"r")
		for line in f:
			words = line.split(" ")
			while "\n" in words: words.remove("\n")
			for word in words:
				self.total_rot += 1
				self.total_words += 1
				if word in dic:
					dic[word] += 1
				else:
					dic[word] = 1
	def calc_prob(self): # replace all dic counters with probailities, returns a list of total prob of fresh and rot words 
		global decimal_shift 
		
		for key in self.dic_fresh:
			self.dic_fresh_prob[key] = (self.dic_fresh[key]/self.total_fresh)*decimal_shift
		for key in self.dic_rot:
			self.dic_rot_prob[key] = (self.dic_rot[key]/self.total_rot)*decimal_shift
		self.f_r_prob.append((self.total_fresh/self.total_words)*decimal_shift) #appending the total fresh probability  fresh words/total words
		self.f_r_prob.append((self.total_rot/self.total_words)*decimal_shift) #appending the total rot probability
	def get_test_words(self,filename):
		words = []
		remove_format(filename)
		f = open(filename, "r")
		for line in f: # this will look for words that are not already recorded and insert them in a list
			toks = line.split(" ")
			while "\n" in toks: toks.remove("\n")
			for tok in toks:
				if tok not in words:
					words.append(tok)
		return words
	def test_results(self,filename):
		global decimal_shift
		words = self.get_test_words(filename)  
		f_r_prob = self.f_r_prob
		prod_fresh = 1
		prod_rot = 1 
		for key in self.dic_fresh:
			if key in words: # if the fresh word is not in it smooth it out as unknown and drop it from calculation 
				prod_fresh = prod_fresh * self.dic_fresh_prob[key]
		self.result_fresh = (prod_fresh* f_r_prob[0]) 
		
		for key in self.dic_rot:
			if key in words: # if the rot word is not in it smooth it out as unknown and drop it from calculation 
				prod_rot = prod_rot * self.dic_rot_prob[key]
		self.result_rot = (prod_rot* f_r_prob[1]) 
	def print_results(self):
		print("Probability of Review being Fresh:" + str(self.result_fresh))
		print("Probability of Review being Rotten:" + str(self.result_rot))
		if self.result_fresh > self.result_rot:
			print("The review is Fresh")
		elif self.result_fresh == self.result_rot:
			print("Result is Neutral")
		else:
			print("The review is Rotten")	
	def print_data(self):
		print("---------------------------------------------")
		print("Total Fresh Words:" + str(self.total_fresh) + " Total Fresh Probability:" + str(self.f_r_prob[0]))
		print("---------------------------------------------")
		print("Fresh Word Data:")
		for key in self.dic_fresh:
			print('word:' + str(key.encode('ascii', 'ignore')) + ' count:' + str(self.dic_fresh[key]) + ' probability:' + str(self.dic_fresh_prob[key]))	
		print("---------------------------------------------")
		print("Total Rotten Words:" + str(self.total_rot) + " Total Rotten Probability:" + str(self.f_r_prob[1]))
		print("---------------------------------------------")
		print("Rotten Word Data:")
		for key in self.dic_rot:
			print('word:' + str(key.encode('ascii', 'ignore')) + ' count:' + str(self.dic_rot[key]) + ' probability:' + str(self.dic_rot_prob[key]))			
		print("---------------------------------------------")	 
def main(args):
	global freshName, rottenName, test_name
	try:
		freshName = args[2]
		rottenName = args[4]
		test_name = args[6]
	except NameError:
		print('did not have enough arguments!')
		sys.exit()
			
	reviews = fresh_count(freshName,rottenName)
	reviews.read_to_fresh_dic() 
	reviews.read_to_rot_dic()
	reviews.calc_prob()
	reviews.print_data()
	reviews.test_results(test_name)
	reviews.print_results()
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

