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
import re
from collections import Counter

VOWELS = 'aeiou'
VOWELS_PATTERN = "['a','e','i','o','u']"
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALL_LETTERS = VOWELS + CONSONANTS
HAND_SIZE = 7
WILDCARD = '*'
GAME_OVER = '!!'

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
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

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score_1 = 0
    for letter in word:
        score_1 += SCRABBLE_LETTER_VALUES.get(letter, 0)
    word_length = len(word)
    return score_1 * max(1, HAND_SIZE * word_length - 3 * (n - word_length))


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    hand: dictionary (string -> int)
    """
    print('Current Hand: ', end=' ')
    for letter in hand.keys():
        for _ in range(hand[letter]):
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
    hand = {WILDCARD: 1}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

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
    new_hand = {}
    # check all letter in hand
    for key in hand.keys():
        if key in word:
            counter = hand[key] - word.count(key)
            if counter > 0:
                new_hand[key] = counter
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
    pattern = word
    word_dict = dict(Counter(word))
    word_set = set(word)
    # check is all letters from word set in intersection
    if set(hand.keys()).intersection(word_set) == word_set:
        # check is letters in word not too much
        for letter in word_set:
            if hand[letter] < word_dict[letter]:
                return False
        # check is wildcard in word
        if WILDCARD in word:
            pattern = word.replace(WILDCARD, VOWELS_PATTERN)
        # check is word in wordlist
        if re.search(pattern, str(word_list)):
            return True
    return False


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
    total = 0
    # As long as there are still letters left in the hand:
    while hand:
        display_hand(hand)
        print()
        word = input('Enter word, or “!!” to indicate that you are finished: ')
        word = word.lower()
        if GAME_OVER == word:
            break
        else:
            if is_valid_word(word, hand, word_list):
                word_total = get_word_score(word, len(hand))
                total += word_total
                print(f'“{word}” earned {word_total} points. Total: {total} points')
            else:
                print('This is not a valid word. Please choose another word.')
            print()
        hand = update_hand(hand, word)
    # Game is over (user entered '!!' or ran out of letters),
    if GAME_OVER != word:
        print('Ran out of letters')
    print(f'Total score for this hand: {total}')
    return total


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int) 
    """
    all_hands_letters = hand.keys()
    # here we check is all vowels letters in hand, or no. If all, return hand without changing
    if letter not in all_hands_letters or set(all_hands_letters).intersection(set(VOWELS)) == set(VOWELS):
        return hand
    # choose random letter
    random_letter = random.choice(ALL_LETTERS)
    # while letter also in hand, we choose other random letter
    while random_letter in all_hands_letters:
        random_letter = random.choice(ALL_LETTERS)
    # make new_hand and changed it
    new_hand = hand.copy()
    new_hand[random_letter] = new_hand[letter]
    # remove old letter
    del (new_hand[letter])
    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    word_list: list of lowercase strings

    return: the total score for the series of hands
    """
    total_score = 0
    play_games_count = ask_user_total_number()
    while play_games_count != 0:
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        print()
        is_substitute_hand = ask_user_yes_no('Would you like to substitute a letter? ')
        if is_substitute_hand == "yes":
            which_letter = ask_user_letter('Which letter would you like to replace: ')
            hand = substitute_hand(hand, which_letter)
        score_first = play_hand(hand, word_list)
        print('--------')
        score_second = replay_hand(hand, word_list)
        if not score_second:
            total_score += score_first
        else:
            total_score += score_second
        play_games_count -= 1
    print('--------')
    print(f'Total score over all hands: {total_score}')


def replay_hand(hand, word_list):
    '''
    Function for replay hand game, if user want.
    hand: dict, dict with letters
    word_list: string, all words

    return: total score for game
    '''
    is_replay_hand = ask_user_yes_no('Would you like to replay the hand? ')
    if is_replay_hand == 'yes':
        total = play_hand(hand, word_list)
        return total
    else:
        return 0


def ask_user_total_number():
    '''
    Function for checking valid/invalid inputing. Ask total number.
    question: string, what user input

    return: string, valid item
    '''
    try:
        count = int(input('Enter total number of hands: '))
        if count > 0:
            return count
        else:
            print('Total number must be greater than zero.')
            return ask_user_total_number()
    except:
        print('Total number should be natural.')
        return ask_user_total_number()


def ask_user_yes_no(question):
    '''
    Function for checking valid/invalid inputing. Ask yes-no.
    question: string, what user input

    return: string, valid item
    '''
    reaction = (input(question)).replace(' ', '')
    while reaction != 'yes' and reaction != 'no':
        print('Please, write yes or no.')
        reaction = (input(question)).replace(' ', '')
    return reaction


def ask_user_letter(question):
    '''
    Function for checking valid/invalid inputing. Ask a letter.
    question: string, what user input

    return: string, valid item
    '''
    letter = (input(question)).replace(' ', '')
    while not letter.isalpha() or len(letter) != 1:
        print('Please, write only one letter.')
        letter = (input(question)).replace(' ', '')
    return letter


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
