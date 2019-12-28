This code was created by Nicholas Vaughn 
AI Class COMP 151 - Project 3: Bayesian Learning

created in Python 3.5.2
Make sure to use Python3
Here's how to run the file 
python mainBay.py -f train_fresh.txt -r train_rotten.txt -t review_fresh.txt

MAKE SURE to have the exact sequence for the flags above, it doesnt adapt to changing them around 

after -f flag you put the name of the training file for fresh reviews
after -r flag you put the name of the training file for rotten reviews
after -t flag you put the name of the review file you want to test

I have global variables for all of these, if you would rather use the gloabl varibals instead of the arguments
then commnet out this chunk of code in main.

	try:
		freshName = args[2]
		rottenName = args[4]
		test_name = args[6]
	except NameError:
		print('did not have enough arguments!')
		sys.exit()

the most important global variable is decimal_shift. This will make reading the data more accurate
with the probabilities values. The value I have was successful with the test files I provided. 

The cleanData.py removes all the formatting for punctuation, and makes all the words lower case with its remove_format function 

If you want a simple example you can run this line 

python mainBay.py -f example_fresh.txt -r example_rotten.txt -t test_ex_fresh.txt

if you want to print to a text file

python mainBay.py -f example_fresh.txt -r example_rotten.txt -t test_ex_fresh.txt >output.txt

Side note: the files with the words copy in it are the original files that have never been formated, 
the current text files have gone through my remove format function before