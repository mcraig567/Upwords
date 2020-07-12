# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 11:18:34 2020

@author: craig
"""

"""
Check if word can be played
- Are all letters to be played in the player's hand
- Does the word go off the edge of the board
- Are all tiles being played on still valid tiles
- Do any of the letters get played on the same letter
- Are all new words real words

All checks to return True if okay, False if not okay
"""

from config import MAXHEIGHT, WIDTH, LENGTH, HANDSIZE

def check_hand(word, hand):
    """Checks the user's hand to ensure all letters in the word are available to play"""
    
    hand_copy = hand
    
    for letter in word:
        if letter not in hand_copy:
            print("ERROR --- Letters not in hand")
            return False
        else:
            hand_copy = hand_copy.replace(letter, '', 1)
    
    print("Hand Check --- Pass")    
    return True

def check_location(word, location, orientation):
    """Checks the location of the letters played, ensuring they will fit on the board"""
    
    #Playing the QU tile reduces length of word by 1
    location_word_len = len(word)
    if "q" in word:
            location_word_len -= 1
    
    #Horizontal Words
    if orientation == 1:
        if location[1] + location_word_len > WIDTH:
            print("ERROR --- Word goes off board (Too far right)")
            print("Word:", word)
            print("Start Location:", location)
            print("Last letter at: ", location[1] + location_word_len)
            return False
        else:
            print("Location Check --- Pass")
            return True
    
    #Vertical Words    
    else:
        if location[0] + location_word_len > LENGTH:
            print("ERROR --- Word goes off board (Too far down)")
            print("Word:", word)
            print("Start Location:", location)
            print("Last letter at: ", location[0] + location_word_len)
            return False
        else:
            print("Location Check --- Pass")
            return True
        
def check_heights(word, location, orientation, tiles):
    """Checks the height of each tile, ensuring that letters can still be played on each tile"""
    
    #Horizontal Words
    if orientation == 1:
        for i in range(len(word)):
            for tile in tiles:
                if tile.get_location() == (location[0], location[1] + i):
                    if not tile.get_valid():
                        print("ERROR --- Tiles are maxed out")
                        return False                    
        print("Height Check --- Pass")
        return True
    
    #Vertical Words
    else:
        for i in range(len(word)):
            for tile in tiles:
                if tile.get_location() == (location[0] + i, location[1]):
                    if not tile.get_valid():
                        print("ERROR --- Tiles are maxed out")
                        return False
        print("Height Check --- Pass")
        return True
    
def check_plural(location, words, orientation, main_start_tile, acc_start_tile):
    """Ensure that the letter played is not solely to pluralize a word"""

    #Player only played a single tile, at most one accessory word
    if len(words) == 1:
        main_word = words[0]
              
        #Horizontal Word
        if orientation == 1:
            #Player pluralized the word
            if location[1] == main_start_tile.get_location()[1] + len(main_word) - 1:
                return False
            
            #s not played at end of word
            else:
                return True
        
        #Vertical Word
        else:
            #Player pluralized the word
            if location[0] == main_start_tile.get_location()[0] + len(main_word) - 1:
                return False
            
            #s not played at end of word
            else:
                return True
            
    #There is an accessory word    
    else:
        main_word = words[0]
        acc_word = words[1]
        
        #Horizontal Word
        if orientation == 1:
            #Player pluralized the main word
            if location[1] == main_start_tile.get_location()[1] + len(main_word) - 1:
                #Player also pluralized the accessory word
                if location[0] == acc_start_tile.get_location()[0] + len(acc_word) - 1:
                    return False
                #Player made a real move on the accessory word
                else:
                    return True
            
            #The s was not played at the end of the word    
            else:
                return True
        
        #Vertical word
        else:
            #Player pluralized the main word
            if location[0] == main_start_tile.get_location()[0] + len(main_word) - 1:
                #Player also pluralized the accessory word
                if location[1] == acc_start_tile.get_location()[1] + len(acc_word) - 1:
                    return False
                #Player made a real move on the accessory word
                else:
                    return True
            
            #The s was not played at the end of the main word
            else:
                return True
                
#Function to run all initial checks in one call
def initial_checks(word, hand, location, orientation, tiles):
    """
    Combines check_hand, check_location, and check_heights into a single function
    """
    
    cHand = check_hand(word, hand)
    cLoc = check_location(word, location, orientation)
    cHeight = check_heights(word, location, orientation, tiles)

    if cHand and cLoc and cHeight:
        return True
    else:
        return False
    
def check_repeats(word, location, orientation, tiles):
    """Checks to see if player is placing a letter on the same letter (ex. playing 'a' on 'a')"""
    
    #Horizontal Words
    if orientation == 1:
        for i in range(len(word)):
            for test_tile in tiles:
                if test_tile.get_location() == (location[0], location[1] + i):
                    if test_tile.get_letter() == word[i]:
                        return False
                    
    #Vertical Words
    else:
        for i in range(len(word)):
            for test_tile in tiles:
                if test_tile.get_location() == (location[0] + i, location[1]):
                    if test_tile.get_letter() == word[i]:
                        return False        

    return True    
    
def touch_check(word, main_word, acc_words):
    """
    Determine if the word played is touching any other words, or if a single letter was added to an exisiting word
    word (str) is the letters played this turn
    main_word (list of str) is the complete word created by the user, in the direction specified by the user
    acc_words (list of str) is all the words (or letters) created in the opposite direction
    Returns True if valid move, False if not  
    """
    
    #Check to see if existing word was extended
    if len(main_word[0]) > len(word):
        #print("Touch Check --- Pass")
        return True
    
    # #Single tile is played, must extend an existing word, or be played on top of an existing tile
    # elif len(word) == 1:
    #     if len(main_word[0]) == 1:
    #         print("ERROR --- Cannot play a single lone tile")
    #         return False
    #     else:
    #         print("Touch Check --- Pass")
    #         return True
        
    #Multiple tiles played, not changing an existing word
    else:
        len_check = False
        
        #Iterate through accesory words
        for acc in acc_words:
            
            #If any accesory word is greater than length 1, than it's touching an existing tile
            if len(acc) > 1:
                #print("Touch Check --- Pass")
                len_check = True
                
        return len_check
    
def check_word(word, wordList):
    """"Check to see if a word is in the wordlist"""
    
    if word.lower() in wordList:
        print("Word Check --- Pass")
        return True
    else:
        print("Error --- ", word, " is not a real word")
        return False
        