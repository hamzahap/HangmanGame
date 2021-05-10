from random import randint
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox
import time
import threading

# getInfile()
# Gets a text file containing words to be chosen by the Hangman program
def getInfile():
	try:
		# First, we check for a file called "wordlist.txt". If it exists in the same directory
		#	as the Hangman program, then we use this file as our word list automatically
		with open('wordlist.txt', 'r'): infile_name = 'wordlist.txt'
	except IOError:
		# If wordlist.txt cannot be found, then we ask the user to specify a text file
		found_file = False
		infile_name = input('Please specify a text file containing a list of words for the Hangman game to choose from (include the full file path if the file is in a different directory than the Hangman program): ')
		# If the user specifies a file name of a file that cannot be found, we keep asking for
		#	a valid input file until a valid one is specified
		while not(found_file):
			try:
				with open(infile_name, 'r'): found_file = True
			except IOError:
				infile_name = input('\n{0} was not found!\n\nPlease try again, or specify a different file (include the full file path if the file is in a different directory than the Hangman program): '.format(infile_name))

	return infile_name

# Chooses a word randomly from the list of words taken from the input file
def chooseWord(infile_name, wordLen):
	infile = open(infile_name, 'r')
	wordlist = infile.readlines()
	total_words = len(wordlist)
	random_num = randint(0, total_words - 1)
	chosen_word = wordlist[random_num].replace('\n', '')
	word_len = len(chosen_word)
	if(wordLen > 0):
		while(word_len != wordLen):
			random_num = randint(0, total_words - 1)
			chosen_word = wordlist[random_num].replace('\n', '')
			word_len = len(chosen_word)
	return chosen_word, word_len

def timer(gamelabel1, game, hiddenword, progressBar):
    wordprint = '';
    while(gameRunning.get() == True):
          if(messageBoxOpen.get() == False):
            if(startTime.get()<=0):
                start_time = time.time();
                startTime.set(10);
                remainingguesses.set(remainingguesses.get() - 1);
                showhangman(gamelabel1,remainingguesses)
                wordprint = "Incorrect Guesses Remaining: " + str(remainingguesses.get()) + "\n"
                hiddenword.set(wordprint)
                progressBar["value"] = startTime.get()*10;
                game.update();
                if(remainingguesses.get() <=0):
                   lose(game, word)
            time.sleep(1);
            startTime.set(startTime.get()-1);
            progressBar["value"] = startTime.get()*10;
            game.update();

def letterguess(guessfield,pointsAvailable, hiddenword,hiddenword1, game, gamelabel1, man):
	global correctcounter
	global incorrectcounter
	global wordarray
	global guessedletters
	global word
	global letters
	global end
	i = 0
	letterinword = False
	startTime.set(10);
	valid = True
	letter = guessfield.get()
	letter = letter.lower()
	guessfield.delete(0, END)
	## account for blank input ##
	if (len(letter) == 0):
		messagebox.showinfo("Error", "Please enter a letter!")
		valid = False
	if(letter in guessedletters):
		messagebox.showinfo("Error", "Letter has already been guessed");
		valid = False
	if(len(letter) > 1):
		messagebox.showinfo("Error", "Enter a single charecter!");
		valid = False
	## check to see if letter is good ##
	while (i < len(word) and valid):

		if word[i] == letter[0]:
			letterinword = True
			wordarray.pop(2*i)
			wordarray.insert(2*i, letter[0])
			scr.set(scr.get()+1) 
			val.set(str("Score: " + str(scr.get())));

		i = i + 1

	## incorrect guess ##
	if (not letterinword and valid):

		if guessedletters.count(letter[0]) == 0:
			guessedletters.append(letter[0])
			remainingguesses.set(remainingguesses.get() - 1)

	## update label ##
	wordprint = ''.join(wordarray) + "\n"
	wordprint = wordprint + "Guessed Letters: " + ', '.join(guessedletters) + "\n"
	hiddenword1.set(wordprint);

	wordprint = '';
	wordprint = wordprint + "Incorrect Guesses Remaining: " + str(remainingguesses.get()) + "\n"
	hiddenword.set(wordprint)


	## update image ##
	showhangman(gamelabel1,remainingguesses)

	## win condition ##
	if correctcounter == len(word):
		win(game, word)

	## lose condition ##
	if remainingguesses.get() <= 0:
		lose(game, word)

## word guess section ##
def wordguess(guessfield, hiddenword, game, man):

	global word
	wordguess = guessfield.get()
	i = 0
	match = True

	if (len(wordguess) == 0):
		match = False

	while i < len(wordguess):
		if word[i] != wordguess[i]:
			match = False
		i = i + 1

	if len(word) != len(wordguess):
		match = False

	if match:
		win(game, word)
	else:
		lose(game, word)


## play the actual game ##
def hint(object):
	messageBoxOpen.set(True);
	startTime.set(10);
	for letter in word:
		if(letter not in guessedletters):
			messagebox.showinfo("Hint", "The Hint is " + letter);
			break;
	startTime.set(10);
	messageBoxOpen.set(False);
	object.pack_forget();

def startgame():
	global word
	global wordLen;
	try:
		wordLen = int(wordlenfield.get());
	except:
		wordLen = 0;
	infile_name = getInfile()
	# Choose a word at random from the acquired word list
	word, word_len = chooseWord(infile_name,wordLen)

	if word_len < 1:
		messagebox.showinfo("Error", "Please enter a word!")
		startgame()

	gameRunning.set(True);
	startTime.set(10);
	## lots of variables for actual game ##
	remainingguesses.set(9);

	global wordarray
	global pointsAvailable
	global guessedletters
	pointsAvailable = StringVar();
	wordarray = []
	guessedletters = []
	i = 0
	while i < word_len:
		wordarray.append('_')
		wordarray.append(' ')
		i = i + 1

	global correctcounter
	global incorrectcounter
	correctcounter = 0
	incorrectcounter = 0
	## end variables ##


	game = Toplevel()
	game.wm_title("Hangman")
	game.minsize(100,100)
	game.geometry("500x520")

	man = PhotoImage(file="gallows.gif")
	hiddenword = StringVar()
	hiddenword1 = StringVar()


	gamelabelfiller = Label(game, text = "Timer:")
	gamelabelfiller.pack()
	progressBar=ttk.Progressbar(game,length=100,orient='horizontal',mode='determinate')
	progressBar.pack()

	gamelabel1 = Label(game, image=man)
	gamelabel1.image = man
	gamelabel1.pack()

	gamelabel3 = Label(game, textvariable=pointsAvailable)
	gamelabel3.pack()

	gamelabel4 = Label(game, textvariable=hiddenword)
	gamelabel4.pack()

	gamelabel2 = Label(game, textvariable=hiddenword1)
	gamelabel2.pack()

	guessfield = Entry(game)
	guessfield.pack()

	pointsAvailable.set("Your Total Points : " + str(word_len - correctcounter));
	remainingguesses.set(remainingguesses.get() - incorrectcounter)

	wordprint = ''.join(wordarray) + "\n"
	wordprint = wordprint + "Guessed Letters: " + ', '.join(guessedletters) + "\n"
	hiddenword1.set(wordprint); 

	wordprint = '';
	wordprint = wordprint + "Incorrect Guesses Remaining: " + str(remainingguesses.get()) + "\n"
	hiddenword.set(wordprint)

	t = threading.Timer(0, timer,kwargs={'gamelabel1': gamelabel1,'game':game, 'hiddenword':hiddenword, 'progressBar': progressBar});
	t.daemon = True;
	t.start();

	bguessletter = Button(game, text="Guess Letter", width=15, command=lambda:
		letterguess(guessfield, pointsAvailable, hiddenword, hiddenword1, game, gamelabel1, man))
	bguessletter.pack()

	bhint = Button(game, text="Get Hint", width=15, command=lambda:
		hint(bhint))
	bhint.pack()

	bguessword = Button(game, text="Guess Word [ONE CHANCE]", width=25, command=lambda:wordguess(guessfield, hiddenword, game, man))
	bguessword.pack()

	game.mainloop()

## quit the game ##
def quitnow():
        global root
        messagebox.showinfo("Hangman in Python", "Thanks for playing! See you soon!")
        root.destroy()

def win(game, word):
	gameRunning.set(False);
	messagebox.showinfo("Winnerx2-Chicken-Dinner", "You WIN! The word was " + word + "!")
	game.withdraw()

def lose(game, word):
	gameRunning.set(False);
	messagebox.showinfo("Loser-Shmooser", "You LOSE! The word was " + word + "!")
	game.withdraw()

def showhangman(gamelabel1,remainingguesses):
	print("Hangman");
	print(str(remainingguesses.get()));
	if remainingguesses.get() == 9:
		img = PhotoImage(file="gallows.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 8:
		img = PhotoImage(file="head.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 7:
		img = PhotoImage(file="noarms.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 6:
		img = PhotoImage(file="rightarm.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 5:
		img = PhotoImage(file="nolegs.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 4:
		img = PhotoImage(file="almostdead.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 3:
		img = PhotoImage(file="dead.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 2:
		img = PhotoImage(file="deader.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 1:
		img = PhotoImage(file="moredead.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses.get() == 0:
		img = PhotoImage(file="deadest.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img


root = Tk()
root.wm_title("Hangman in Python")
root.minsize(380,380)
root.geometry("300x100")

title = PhotoImage(file="title.gif")
titleLabel = Label(root, image=title)
titleLabel.image = title
titleLabel.pack()
startTime = IntVar();
startTime.set(10);

x = Label(root, text="Word Length")
x.pack()

gameRunning = BooleanVar();
gameRunning.set(True);

messageBoxOpen = BooleanVar();
messageBoxOpen.set(False);

scr = IntVar();
scr.set(0);

val = StringVar();
val.set(str("Score: " + str(scr.get())));

wordlenfield = Entry(root)
wordlenfield.pack()

remainingguesses = IntVar()
score = Label(root, textvariable=val);
score.pack();

bplay = Button(root, text="Play", width=10, command=startgame)
bplay.pack()

bquit = Button(root, text="Quit", width=10, command=quitnow)
bquit.pack()

mainloop()
