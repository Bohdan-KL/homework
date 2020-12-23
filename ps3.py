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
ALL_LETTERS = VOWELS + CONSONANTS
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
        
    del (hand[x])
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
    total = 0
    # As long as there are still letters left in the hand:
    while hand:
        print(display_hand(hand))
        word = input('Enter word, or “!!” to indicate that you are finished: ')
        if '!!' in word:
            break
        else:
            if is_valid_word(word, hand, word_list):
                word_total = get_word_score(word, len(hand))
                total += word_total
                print(f'“{word}” earned {word} points. Total: {total} points')
            else:
                print('This is not a valid word. Please choose another word.')
            print()
        hand = update_hand(hand, word)
    # Game is over (user entered '!!' or ran out of letters),
    if '!!' in word:
        print(f'Total score for this hand: {total}')
    else:
        print('Ran out of letters')
        print(f'Total score for this hand: {total}')
    return total


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int) or string(if all letters in hand)
    """
    all_hands_letters = hand.keys()
    if letter not in all_hands_letters:
        return hand
    elif len(all_hands_letters) == 27 and '*' in all_hands_letters:
        return 'Cannot be replaced, all letters are here.'
    elif len(all_hands_letters) == 26 and '*' not in all_hands_letters:
        return 'Cannot be replaced, all letters are here.'
    random_letter = random.choice(ALL_LETTERS)
    while random_letter in all_hands_letters:
        random_letter = random.choice(ALL_LETTERS)
    new_hand = hand.copy()
    new_hand[random_letter] = new_hand[letter]
    del (new_hand[letter])
    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    word_list: list of lowercase strings

    return: the total score for the series of hands
    """
    total_score = 0
    play_games_count = ask_user('Enter total number of hands: ')
    while play_games_count != 0:
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        print()
        is_substitute_hand = ask_user('Would you like to substitute a letter? ')
        if is_substitute_hand == "yes":
            which_letter = ask_user('Which letter would you like to replace: ')
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
    is_replay_hand = ask_user('Would you like to replay the hand? ')
    total = False
    while is_replay_hand == 'yes':
        total = play_hand(hand, word_list)
        print('--------')
        is_replay_hand = ask_user('Would you like to replay the hand? ')
    return total


def ask_user(question):
    '''
    Function for checking valid/invalid inputing.
    question: string, what user input

    return: string, valid item
    '''
    if question == 'Enter total number of hands: ':
        try:
            count = int(input('Enter total number of hands: '))
            if count > 0:
                return count
            else:
                print('Total number must be greater than zero.')
                return ask_user(question)
        except:
            print('Total number should be natural.')
            return ask_user(question)
    elif question == 'Would you like to substitute a letter? ' or question == 'Would you like to replay the hand? ':
        reaction = (input(question)).replace(' ', '')
        while reaction != 'yes' and reaction != 'no':
            print('Please, write yes or no.')
            reaction = (input(question)).replace(' ', '')
        return reaction
    elif question == 'Which letter would you like to replace: ':
        letter = (input(question)).replace(' ', '')
        while not letter.isalpha() or len(letter) != 1:
            print('Please, write only one letter.')
            letter = (input(question)).replace(' ', '')
        return letter


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
