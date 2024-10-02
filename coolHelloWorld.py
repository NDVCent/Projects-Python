import random
import string
import time

letters = string.ascii_letters + " "
target = "Hello World" #the sentence or world that must be in the result 
result = ""
	
for letter in target:
	while True:
		I = random.choice(letters)
		print(result + I)
		if (I == letter):
			result += I
			break
		time.sleep(0.009)