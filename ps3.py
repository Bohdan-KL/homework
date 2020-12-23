# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Bohdan Klots
# Collaborators : Victor Hozhyi
# Time spent    : <total time>

import math
import random
from collections import Counter

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    return dict(Counter(sequence))


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()
    score_1 = 0
    for i in word:
        score_1 += SCRABBLE_LETTER_VALUES.get(i, 0)
    word_length = len(word)
    score_2 = max(1, 7 * word_length - 3 * (n - word_length))
    return score_1 * score_2


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    hand: dictionary (string -> int)
    """
    print('Current Hand: ', end=' ')
    for letter in hand.keys():
        for j in range(hand[letter]):
            # print all on the same line
            print(letter, end=' ')
    return ''


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    del hand[x]
    hand["*"] = 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word = word.lower()
    new_hand = hand.copy()
    remover = set()
    for key in new_hand.keys():
        if key in word:
            counter = max(0, new_hand[key] - word.count(key))
            if counter == 0:
                remover.add(key)
            else:
                new_hand[key] = counter

    for key in remover:
        del new_hand[key]

    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()

    working_hand = hand.copy()
    keys = working_hand.keys()

    for letter in word:
        if letter not in keys or working_hand[letter] == 0:
            return False
        else:
            working_hand[letter] -= 1
            if letter == '*':
                ind = word.index('*')
                for vowel in VOWELS:
                    if word[:ind] + vowel + word[ind + 1:] in word_list:
                        return True
    return word in word_list


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    return sum(hand.values())


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total = 0

    # As long as there are still letters left in the hand:
    while hand:

        # Display the hand
        print(display_hand(hand))
        # Ask user for input
        word = input('Enter word, or “!!” to indicate that you are finished: ')

        # If the input is two exclamation points:
        if '!!' in word:

            # End the game (break out of the loop)
            break

        # Otherwise (the input is not two exclamation points):
        else:

            # If the word is valid:
            if is_valid_word(word, hand, word_list):

                # Tell the user how many points the word earned,
                # and the updated total score
                word_total = get_word_score(word, len(hand))
                total += word_total
                print(f'“{word}” earned {word} points. Total: {total} points')

            # Otherwise (the word is not valid):
            # Reject invalid word (print a message)
            else:
                print('This is not a valid word. Please choose another word.')
            print()
        # update the user's hand by removing the letters of their inputted word
        hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if '!!' in word:
        print(f'Total score: {total} points')
    else:
        print(f'Ran out of letters. Total score: {total} points')

    # Return the total score as result of function
    return total


play_hand(deal_hand(7), load_words())




def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    pass  # TO DO... Remove this line when you implement this function


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    print("play_game not implemented.")  # TO DO... Remove this line when you implement this function

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#

# if __name__ == '__main__':
#    word_list = load_words()
#    play_game(word_list)
