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

------------------------------------------------------------

Movie Review Mood Arcade (FastAPI + React)
==========================================

This project now ships with an optional full-stack playground that wraps the
classic Naive Bayes classifier in a colourful interface.

Backend (FastAPI)
-----------------

* Location: `backend/app`
* Install dependencies: `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`
* Launch locally: `uvicorn app.main:app --reload`
* Helpful endpoints:
  * `GET /ping` health check
  * `POST /train` to retrain the classifier. Accepts optional custom snippets and
    Laplace smoothing value.
  * `POST /classify` to score a free-form review and return fresh/rotten probabilities.

Frontend (React + Vite + TypeScript)
------------------------------------

* Location: `frontend`
* Copy `.env.example` to `.env` and tweak `VITE_API_BASE_URL` if the backend runs
  on a custom host/port.
* Install dependencies: `npm install`
* Start the development server: `npm run dev`
* Build for production: `npm run build`

Fun tour of the interface:

* **Home** – Explains the project lore and how the tabs fit together.
* **Training Lab** – Mix your own fresh/rotten snippets, toggle smoothing, and
  retrain the FastAPI service. Distinctive words are highlighted after training.
* **Classifier Arcade** – Paste any movie review to see a probability duel and a
  running history of verdicts.

Feel free to keep using the original CLI workflow (`mainBay.py`) if you prefer –
both experiences co-exist happily.