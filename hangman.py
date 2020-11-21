# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    return set(letters_guessed).intersection(set(secret_word)) == set(secret_word)  # Discrete Math is the best.


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    result = ''
    for i in secret_word:
        result += i if i in letters_guessed else "_ "
    return result
    # it's not the most fast, but I think here fast is not very important(words are small)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    return "".join(sorted(list(set(string.ascii_lowercase).difference(set(letters_guessed)))))
    # Functional programming and discrete mathematics 💪🙂


def if_bad(key, warnings_remaining, guesses_remaining, guessed_word):
    '''
    It's function for checking not normal inputs.
    '''
    if key == 1:
        if warnings_remaining != 0:
            warnings_remaining -= 1
            print(f'Oops! That is not a valid letter. You have {warnings_remaining} '
                  f'warnings left: {guessed_word}\n-------------')
        else:
            guesses_remaining -= 1
            print(
                f'Oops! That is not a valid letter. You have no warnings left so you '
                f'lose one guess: {guessed_word}\n-------------')
    else:
        if warnings_remaining != 0:
            warnings_remaining -= 1
            print(
                f'Oops! You have already guessed that letter. You have {warnings_remaining} '
                f'warnings left: {guessed_word}\n-------------')
        else:
            guesses_remaining -= 1
            print(
                f'Oops! You have already guessed that letter. You have no warnings left so you '
                f'lose one guess: {guessed_word}\n-------------')
    return warnings_remaining, guesses_remaining, guessed_word


def inform_and_input(guesses_remaining, available_letters):
    '''
    interactive_game should be small
    '''
    print(f'You have {guesses_remaining} guesses left.')
    print(f'Available letters: {available_letters}')
    return input('Please guess a letter: ')


def interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, guessed_word,
                     available_letters, with_hints):
    '''
    It is the interactive game or main part of hangman function.
    '''
    if not guesses_remaining:
        return print(f'Sorry, you ran out of guesses. The word was {secret_word}')
    letter = inform_and_input(guesses_remaining, available_letters)
    if letter == '*' and with_hints:
        show_possible_matches(guessed_word)
    elif not str.isalpha(letter):
        warnings_remaining, guesses_remaining, guessed_word = if_bad(1, warnings_remaining, guesses_remaining,
                                                                     guessed_word)
    elif str.lower(letter) in letters_guessed:
        warnings_remaining, guesses_remaining, guessed_word = if_bad(2, warnings_remaining, guesses_remaining,
                                                                     guessed_word)
    else:
        letter = str.lower(letter)
        letters_guessed.append(letter)
        available_letters = get_available_letters(letters_guessed)
        if guessed_word == get_guessed_word(secret_word, letters_guessed):
            if letter in 'aeiou':
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            print(f'Oops! That letter is not in my word: {guessed_word}\n-------------')
        else:
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print(f'Good guess: {guessed_word}\n-------------')
            if is_word_guessed(secret_word, letters_guessed):
                return print(
                    f'Congratulations, you won! Your total score for this game is: '
                    f'{len(secret_word) * guesses_remaining}')
    interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, guessed_word,
                     available_letters, with_hints)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    warnings_remaining, guesses_remaining = 3, 6
    letters_guessed = []
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    available_letters = get_available_letters(letters_guessed)
    print("Welcome to the game Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left.')
    print("-------------")
    with_hints = False
    interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, guessed_word,
                     available_letters, with_hints)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------
def replace(x):
    '''
    A small function for change list
    '''
    return '' if x == ' ' else x


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word = "".join(list(my_word.split(' ')))
    if len(my_word) != len(other_word):
        return False
    elif '_' in my_word and set(my_word) == set(other_word + '_'):
        return False
    else:
        length = len(my_word) + 1
        for i in range(length):
            if my_word[i:i + 1] != other_word[i:i + 1] and my_word[i:i + 1] != '_':
                if my_word[i:i + 1] != '':
                    return False
    return True


def show_possible_matches(my_word, sourse=wordlist):  # I added here the sourse becouse I don't want to use "global"
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    print('Possible word matches are: ', end='')
    for i in sourse:
        if match_with_gaps(my_word, i):
            print(i, end=' ')
    print('\n--------')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    warnings_remaining, guesses_remaining = 3, 6
    letters_guessed = []
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    available_letters = get_available_letters(letters_guessed)
    print("Welcome to the game Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left.')
    print("-------------")
    with_hints = True
    interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, guessed_word,
                     available_letters, with_hints)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

secret_word = choose_word(wordlist)
hangman_with_hints(secret_word)
