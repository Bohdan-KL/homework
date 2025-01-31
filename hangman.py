# Problem Set 2, hangman.py
# Name: Bohdan Klots
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code

import random
import string
from enum import Enum

WORDLIST_FILENAME = "words.txt"

UNKNOW_LETTER = '_'
INITIAL_WARNIGS = 3
INITIAL_GUESSES = 6
HINTS = "*"
VOWELS = set('aeiou')
VALID_LETTER = string.ascii_lowercase

class ValidationResultType(Enum):
    NOT_CORRECT = 1
    NOT_NEW = 2
    WITH_HINTS = 3
    WITHOUT_HINTS = 4


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
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

    Here used the property of plurals. The program find out intersection of letters_guessed
    plurals and secret_word_set plurals is equal to secret_word_set plurals or no.
    Intersection of two plurals is all elements which is in both plurals.
    Discrete Math is the best.
    '''
    secret_word_set = set(secret_word)
    return letters_guessed.intersection(secret_word_set) == secret_word_set


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = []
    for i in secret_word:
        if i in letters_guessed:
            result.append(i)
        else:
            result.append(UNKNOW_LETTER + " ")
    return ''.join(result)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
      Filter is removing false letters.
    '''
    return "".join(filter(lambda x: x not in letters_guessed, string.ascii_lowercase))


def answer_if_bad(situation, warnings_remaining, guesses_remaining, guessed_word):
    '''
    It's function for checking not normal inputs and printing results.
    situation: View what problem we check. Is not a valid letter(situation = 'not_correct') or user have already guessed
                                                                                    that letter(situation = 'not_new').
    warnings_remaining: how many warnings remaining user have
    guesses_remaining: how many guesses remaining user have
    guessed_word: a guessed word at this moment

    return: changed warnings_remaining, guesses_remaining, guessed_word
    '''
    if situation == ValidationResultType.NOT_CORRECT:
        if warnings_remaining != 0:
            warnings_remaining -= 1
            print(f'Oops! That is not a valid letter. You have {warnings_remaining} '
                  f'warnings left: {guessed_word}')
            print('-------------')
        else:
            guesses_remaining -= 1
            print(
                f'Oops! That is not a valid letter. You have no warnings left so you '
                f'lose one guess: {guessed_word}')
            print('-------------')
    elif situation == ValidationResultType.NOT_NEW:
        if warnings_remaining != 0:
            warnings_remaining -= 1
            print(
                f'Oops! You have already guessed that letter. You have {warnings_remaining} '
                f'warnings left: {guessed_word}')
            print('-------------')
        else:
            guesses_remaining -= 1
            print(
                f'Oops! You have already guessed that letter. You have no warnings left so you '
                f'lose one guess: {guessed_word}')
            print('-------------')
    return warnings_remaining, guesses_remaining, guessed_word


def inform_and_input(guesses_remaining, available_letters):
    '''
    guesses_remaining: parameter for inform user how many guesses remaining he has.
    available_letters: parameter for inform user how many guesses remaining he has.

    return: something what user wrote.

    interactive_game should be small. This function made for making
    interactive_game function smaller and more easy to understand.
    '''
    print(f'You have {guesses_remaining} guesses left.')
    print(f'Available letters: {available_letters}')
    letter = input('Please guess a letter: ').replace(' ', '')
    return letter.lower()


def interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, with_hints):
    '''
    It is the interactive game or main part of hangman function.
    It is the function, which would be run while guesses_remaining is not zero or while
    user not win.

    warnings_remaining: how many warnings remaining user have
    guesses_remaining: how many guesses remaining user have
    guessed_word: guessed word at this moment
    letters_guessed: list (of letters), which letters have been guessed so far
    secret_word: word which computer choose
    available_letters: parameter for inform user how many guesses remaining he has.
    with_hints: True if user is playing with hints, else False

    return: guesses_remaining
    '''
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        # reed the letter
        available_letters = get_available_letters(letters_guessed)
        letter = inform_and_input(guesses_remaining, available_letters)
        # check is user use hint
        if letter == HINTS and with_hints:
            show_possible_matches(guessed_word)
        # chek is user input a correct letter
        elif letter not in VALID_LETTER or len(letter) != 1:
            warnings_remaining, guesses_remaining, guessed_word = answer_if_bad(
                ValidationResultType.NOT_CORRECT, warnings_remaining, guesses_remaining, guessed_word)
        # check is user input a new letter
        elif letter in letters_guessed:
            warnings_remaining, guesses_remaining, guessed_word = answer_if_bad(ValidationResultType.NOT_NEW,
                                                                                warnings_remaining, guesses_remaining,
                                                                                guessed_word)
        # if a letter is new and not invalid, run actions_if_new_letter function
        else:
            letters_guessed, guesses_remaining, guessed_word = actions_if_new_letter(letter, letters_guessed,
                                                                                     guesses_remaining, guessed_word,
                                                                                     secret_word)
    return guesses_remaining


def actions_if_new_letter(letter, letters_guessed, guesses_remaining, guessed_word, secret_word):
    '''
    This function run when letter new and not invalid. Uses only in interactive game.

    letter: it's a letter which user input
    guesses_remaining: how many guesses remaining user have
    guessed_word: guessed word at this moment
    letters_guessed: list (of letters), which letters have been guessed so far

    return: changed letters_guessed, guesses_remaining, guessed_word
    '''
    letter = letter.lower()
    letters_guessed.add(letter)
    # check is a letter in secret word
    if letter not in secret_word:
        if letter in VOWELS:
            guesses_remaining -= 2
        else:
            guesses_remaining -= 1
        print(f'Oops! That letter is not in my word: {guessed_word}')
        print('-------------')
    # if a letter in secret word
    else:
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print(f'Good guess: {guessed_word}')
        print('-------------')
    return letters_guessed, guesses_remaining, guessed_word


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    '''
    warnings_remaining = INITIAL_WARNIGS
    guesses_remaining = INITIAL_GUESSES
    letters_guessed = set()
    print("Welcome to the game Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left.')
    with_hints = is_with_hints()
    if with_hints == ValidationResultType.WITH_HINTS:
        print("You are gaming with hints.")
        print("-------------")
        # total is a variable about how many points of game user have. if 0 - user lose, else - win
        total_points = interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, True)
    else:
        print("You are gaming without hints.")
        print("-------------")
        # total is a variable about how many points of game user have. if 0 - user lose, else - win
        total_points = interactive_game(warnings_remaining, guesses_remaining, letters_guessed, secret_word, False)
    if total_points > 0:
        print(f'Congratulations, you won! Your total score for this game is: '
              f'{len(set(secret_word)) * total_points}')
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')


def is_with_hints():
    '''
    Function for checking valid input. Is game with hints or is without hints.

    Return
    ValidationResultType.WITH_HINTS if 'yes' in reaction, else ValidationResultType.WITHOUT_HINTS
    '''
    print("Do you want to play with hints?")
    reaction = input('Write yes if you want, else write no: ')
    if 'yes' not in reaction and 'no' not in reaction:
        while True:
            print("-------------")
            print('Please, write yes or no')
            reaction = input('Write yes if you want, else write no: ')
            if 'yes' in reaction:
                return ValidationResultType.WITH_HINTS
            elif 'no' in reaction:
                return ValidationResultType.WITHOUT_HINTS
    else:
        if 'yes' in reaction:
            return ValidationResultType.WITH_HINTS
        elif 'no' in reaction:
            return ValidationResultType.WITHOUT_HINTS


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    # compare length
    if len(my_word) != len(other_word):
        return False
    # compare plurals (if found a different letters - return False). Here making checking for all letters
    for my, other in zip(my_word, other_word):
        if my != UNKNOW_LETTER:
            if my != other:
                return False
            elif other_word.count(my) != my_word.count(my):
                return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    result = []
    my_word = my_word.replace(' ', '')
    for word in wordlist:
        if match_with_gaps(my_word, word):
            result.append(word)
    result = ' '.join(result)
    if len(result) > 0:
        print(f'Possible word matches are: {result}')
    else:
        print('There no one possible word matches.')
    print('-------------')


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)
