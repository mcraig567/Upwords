# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 10:44:30 2020

@author: craig

Classes for Upwords
"""

import random
import math

from config import MAXHEIGHT, WIDTH, LENGTH, HANDSIZE

class tile(object):
    """
    Location is the location on the board of the tile
    Letter is the last played letter on the tile. Default to 0 (not played on)
    Height is the number of letters that have been played on the tile. Default to 0
    Valid is if height is below MAXHEIGHT, and letters can still be played on the tile
    """
    def __init__(self, x, y):
        self.location = (x,y)
        self.letter = 0
        self.height = 0
        self.valid = True        

    def get_letter(self):
        return self.letter
    
    def get_location(self):
        return self.location

    def get_height(self):
        return self.height

    def get_valid(self):
        return self.valid

    def check_valid(self):
        #Check valid is done on the turn_copy board, so checking 1 tile more than currently on the board
        if self.height == MAXHEIGHT + 1:
            self.valid = False
            
        return None
    
    def update_letter(self, new_letter):
        self.letter = new_letter
        
        return None
    
    def update_height(self):
        self.height += 1
        
        return None
    
    
    
class player(object):
    """
    Define player class
    Username inputted by user when starting game
    Hand is a string of all the letters in the player's hand
    Score is an int of the user's current score in the game
    Number is an int of the order in which the user was created (First player is number 1)
    """
    
    def __init__(self, username, hand, score, number):
        self.username = username
        self.hand = hand
        self.score = score
        self.number = number
        
    def get_name(self):
        return self.username
        
    def get_hand(self):
        return self.hand
    
    def get_score(self):
        return self.score
    
    def get_number(self):
        return self.number
    
    def update_hand(self, hand, letters):
        hand_length = len(self.get_hand())
        
        #Max hand length is 7 letters, but qu tile is read as 4
        if 'q' in self.hand:
            for i in range(HANDSIZE + 3 - hand_length):
                
                #No more updating once the bag of letters is empty
                if len(letters) > 0:
            
                    #Use random number to determine location in letter list
                    rand = random.random()
                    letter = letters[math.floor(rand*len(letters))]
                    letters.remove(letter)
                    hand = hand + letter 
                    self.hand = hand
        
        #No qu tile in hand
        else:
            for i in range(HANDSIZE - hand_length):
               
                #No more updating once the bag of letters is empty
                if len(letters) > 0:
                
                    #Use random number to determine location in letter list
                    rand = random.random()
                    letter = letters[math.floor(rand*len(letters))]
                    letters.remove(letter)
                    hand = hand + letter 
                    self.hand = hand
           
    def remove_letter(self, hand, letter):
        hand = hand.replace(letter, '', 1)
        self.hand = hand
    
    def update_score(self, wordScore):
        #addest newest word score to total score
        new_score = self.score + wordScore
        self.score = new_score
