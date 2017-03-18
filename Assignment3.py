'''
Assignment 3 - Hash Tables
Sean Remedios - 10190433
The purpose of this assignment is to analyze the differences between quadratic probing and double hashing.
As well as find a minimum table size that satfies the requirement of each insertion operation must look at 
no more than 10 possible locations for the new value.

“I confirm that this submission is my own work and is consistent with the Queen's regulations on Academic Integrity.”
for CISC 235, 18/03/17
'''

import math # Used in the genPrimes function in the GeneratePrimes class

class Read:
	'''
	Function reads the text from a file and creates a list.
	Input:	doc - A text file with strings
	Output:	data - A list of strings, each string is a list of characters
	'''
	def readFile(self, doc):
		data = []
		with open(doc, "r") as in_file:
			for line in in_file:
				newLine = line.rstrip('\n')
				tempList = [] # Initializing a temp list
				for i in newLine:
					tempList.append(i) # Adding each individual character into a temp list 
				#temp = ''.join(tempList) # Joins the list together so it's a string
				data.append(tempList) 
		return data

class GeneratePrimes:
	'''
	Generate a list of primes to find the minimum table size.
	Code taken from http://stackoverflow.com/questions/11619942/print-series-of-prime-numbers-in-python
	Range can be modified for any interval.
	However, 2000 number interval was chosen, with a start value of 2501, because there are 2500 keys and 
	the aim is to find the minimum table size. 
	Output:	primes - A list of prime numbers in a certain interval
	'''
	def genPrimes(self):
		primes = []
		#Only looking at odd numbers
		for num in range(2501,4501,2):
			#Checking if the number is divisible by 2 to sqrt(n)
			if all(num%i!=0 for i in range(2,int(math.sqrt(num))+1)):
				primes.append(num)
		return primes

class HashTable:
	'''
	Initialize the class
	'''
	def __init__ (self, size, const1, const2):
		self.c1 = const1 # 1, 2, 0.5
		self.c2 = const2 # 1, 0.5, 7
		# Primes for double hasing
		# It was noticed that the smaller the primes, the more collisions and insertion fails there were
		self.p1 = 24593
		self.p2 = 12289
		self.tSize = size
		self.hTable = ["empty" for _ in range (size)] # Create an empty hash table

	'''
	Dan Bernstein's djb2 to hash strings to integers. Covered in class.
	Input:	word - A string from the list of strings to be hashed into a key
	Output:	hashdbj2 - A key that was hashed
	'''
	def hashStringToInt(self, word):
		hashdbj2 = 5381 
		for letter in word:
			hashdbj2 = ((hashdbj2 << 5) + hashdbj2) + ord(letter) # Multiplies the hash by 33 and adds the ASCII number
		return hashdbj2 % self.tSize

	'''
	Function uses the hash value of the key to create a new hash value.
	Hash function uses exponentiation of a prime to get a new hash. Doing so requires a lot of time to
	compute since the primes are big and it is being used as an exponent.
	Input:	key - A hashed string value turned into a key by the function hashStringToInt
	Output:	x or x+1 - An odd number that is a new key based off of the other hash
	'''
	def doubleHash(self, key):
		x = (key + self.p1) ** (self.p2) # p1 and p2 are primes
		if (x % 2 == 1):
			return x # Odd
		else:
			return x + 1 # Even + 1 = Odd

	'''
	Function uses quadratic probing to hash a string and insert it into the hash table.
	From the CISC 235 notes. http://sites.cs.queensu.ca/courses/cisc235/Record/20170227%20-%20Quadratic%20Probing.pdf
	Input:	key - A string
	Output:	-1 - Insertion looked at more than 10 possible locations or insertion failed
			0 - Insertion succeeded
	'''
	def insertQP(self, key):
		i = 0
		hashed = self.hashStringToInt(key)
		cpHash = hashed # Copies the actual hash so it can be used
		# Checks if a location is empty
		while ((i < self.tSize) and (self.hTable[cpHash] != "empty") and (self.hTable[cpHash] != "deleted")):
			i += 1
			# Formula for quadratic probing
			cpHash = int((hashed + self.c1*i + self.c2*i*i) % self.tSize)
		# Checks if more than 10 insertion locations were visited
		if (i > 10):
			return -1
		if (self.hTable[cpHash] is "empty" or self.hTable[cpHash] is "deleted"):
			# Found an empty location in the table
			self.hTable[cpHash] = key
		else:
			# Could not insert key into table
			print ("insert failed")
			return -1
		return 0 # Insertion succeeded

	'''
	Modified version of the Quadratic Probing insert function. Uses double hashing to hash a string and insert it into
	the hash table.
	Input:	key - A string
	Output:	-1 - Insertion looked at more than 10 possible locations or insertion failed
			0 - Insertion succeeded
	'''
	def insertDH(self, key):
		i = 0
		hashed = self.hashStringToInt(key)
		doubHash = self.doubleHash(hashed) # Gets a secondary hash from another hash function
		cpHash = hashed
		while ((i < self.tSize) and (self.hTable[cpHash] != "empty") and (self.hTable[cpHash] != "deleted")):
			i += 1
			# Uses first hash and second hash in a formula to create a new hash
			cpHash = int((hashed + i*doubHash) % self.tSize)
		if (i > 10):
			return -1
		if (self.hTable[cpHash] is "empty" or self.hTable[cpHash] is "deleted"):
			self.hTable[cpHash] = key
		else:
			print ("insert failed")
			return -1
		return 0

class mainClass:
	'''
	Main class for quadratic probing hash tables.
	Input:	primes - A list of primes
			data - A list of strings
	'''
	def QP(self, primes, data):
		print("=====QUADRATIC PROBING:=====")
		print("Size:    Constant 1:    Constant 2:")
		# Minimum table sizes that work with each constant pairing
		#		3931         1              1
		#		3943         2              0.5
		#		3943         0.5            7
		for p in primes:
			constants = [[1,1], [2,0.5], [0.5,7]]
			for i in constants:
				# Creates a new instance of the HashTable class (and a new hash table) everytime it's called
				Table = HashTable(p, i[0], i[1]) # i[0] = first number in pairing, i[1] = second number in pairing
				for word in data:
					result = Table.insertQP(word)
					# If statement is useful so we don't have to hash the rest of the keys and can move on to the
					# next constant pairing or next table size. Saves quite a lot of time in the long run.
					if (result == -1):
						break # Checked in more than 10 locations or insertion failed
				if (result == 0):
					print(p, "        ", i[0], "            ", i[1]) # Table size works for particular constant pairing

	'''
	Main class for double hashing hash tables.
	Input:	primes - A list of primes
			data - A list of strings
	'''
	def DH(self, primes, data):
		print("\n=====DOUBLE HASHING:=====")
		print("Note: Program takes awhile to find the first table size that works with a constant pairing")
		print("Size:    Constant 1:    Constant 2:")
		# Minimum table sizes that work with each constant pairing
		# Prime numbers used in double hashing function: 24593 and 12289
		#		3607         1             1
		#		3607         2             0.5
		#		3607         0.5           7
		# NOTE: TAKES A REALLY LONG TIME TO TEST EVERY PRIME UNTIL 5000 WITH EACH SET OF CONSTANTS
		for p in primes:
			# The idea of running simultaneous processes to run each constant pairing for each prime at once
			# was looked into, however it was a bit complicated so now we have to suffer with waiting ages for
			# the minimum table size to come up for every constant.
			constants = [[1,1], [2,0.5], [0.5,7]]
			for i in constants:
				Table = HashTable(p, i[0], i[1])
				for word in data:
					result = Table.insertDH(word)
					if (result == -1):
						break
				if (result == 0):
					print(p, "        ", i[0], "            ", i[1])

def main():
	rClass = Read()
	gP = GeneratePrimes()
	mC = mainClass()
	# Change link if file is not in same directory as program
	data = rClass.readFile('top_secret_agent_codenames_2017.txt')
	primes = gP.genPrimes()

	# Calls the main functions for quadratic probing tables and double hashing tables
	mC.QP(primes, data)
	mC.DH(primes, data)
main()
