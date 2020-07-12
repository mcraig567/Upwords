# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:37:41 2020

@author: craig
"""

from classes import tile, player
from checks import check_hand, check_location, check_heights
from checks import touch_check, check_word
from main import build_tiles


def test_check_hand():
    p1 = player("p1", "qwertyu", 0, 1)
    
    #Test generic case with letters
    test = check_hand("qwer", p1.get_hand())
    assert test == True
    
    #Test generic case without letters
    test = check_hand("qwop", p1.get_hand())
    assert test == False
    
    #Test repeat letters - pass
    p2 = player("p2", "aaabbb", 0, 1)
    test = check_hand("bababa", p2.get_hand())
    assert test == True    

    #Test repeat letters = fail
    test = check_hand("babaaba", p2.get_hand())
    assert test == False
    
def test_check_location_hor():
    #Test middle of board
    test = check_location("the", (3,3), 1)
    assert test == True    
    
    #Test starting on left edge
    test = check_location("the", (3,0), 1)
    assert test == True
    
    #Test ending on right edge
    test = check_location("the", (1,5), 1)
    assert test == True
    
    #Test going off right edge
    test = check_location("the", (1,6), 1)
    assert test == False
    
    #Test single letter played on right edge
    test = check_location("a", (1,7), 1)
    assert test == True
    
def test_check_location_vert():
    #Test middle of board
    test = check_location("the", (3,3), -1)
    assert test == True    
    
    #Test starting on top edge
    test = check_location("the", (0,3), -1)
    assert test == True
    
    #Test ending on bottom edge
    test = check_location("the", (5,1), -1)
    assert test == True
    
    #Test going off bottom edge
    test = check_location("the", (6,1), -1)
    assert test == False
    
    #Test single letter played on bottom edge
    test = check_location("a", (7,1), -1)
    assert test == True
    
def test_check_heights_hor():
    tiles = build_tiles(8,8)
    tiles[27].update_letter('t')
    tiles[27].update_height()
    tiles[28].update_letter('h')
    tiles[28].update_height()
    tiles[29].update_letter('e')
    tiles[29].update_height()
    
    tiles[27].check_valid()
    tiles[28].check_valid()
    tiles[29].check_valid()
    
    #Passing case - All height 1
    test = check_heights("the", (3,3), 1, tiles)
    assert test == True
    
    #Passing case - All height 5
    for i in range(4):
        tiles[27].update_height()
        tiles[28].update_height()
        tiles[29].update_height()
      
    tiles[27].check_valid()
    tiles[28].check_valid()
    tiles[29].check_valid()        
        
    test = check_heights("the", (3,3), 1, tiles)
    assert tiles[27].get_height() == 5
    assert test == True
    
    #Failing case, higher than Max Height (5)
    tiles[27].update_height()
    tiles[27].check_valid()    
    
    test = check_heights("the", (3,3), 1, tiles)
    assert tiles[27].get_height() == 6
    assert test == False
    
def test_check_heights_vert():
    tiles = build_tiles(8,8)
    tiles[27].update_letter('t')
    tiles[27].update_height()
    tiles[35].update_letter('h')
    tiles[35].update_height()
    tiles[43].update_letter('e')
    tiles[43].update_height()
    
    tiles[27].check_valid()
    tiles[35].check_valid()
    tiles[43].check_valid()
    
    #Passing case - All height 1
    test = check_heights("the", (3,3), -1, tiles)
    assert test == True
    
    #Passing case - All height 5
    for i in range(4):
        tiles[27].update_height()
        tiles[35].update_height()
        tiles[43].update_height()
      
    tiles[27].check_valid()
    tiles[35].check_valid()
    tiles[43].check_valid()        
        
    test = check_heights("the", (3,3), -1, tiles)
    assert tiles[27].get_height() == 5
    assert test == True
    
    #Failing case, higher than Max Height (5)
    tiles[27].update_height()
    tiles[27].check_valid()    
    
    test = check_heights("the", (3,3), -1, tiles)
    assert tiles[27].get_height() == 6
    assert test == False
    
def test_touch_check_long():
    
    #Test long word on not touching
    test = touch_check("the", ["the"], ["t", "h", "e"])
    assert test == False
    
    #Test long word played on end of word - opposite direction
    test = touch_check("the", ["the"], ["t", "h", "here"])
    assert test == True
    
    #Test long word played on end of word - same direction
    test = touch_check("the", ["hethe"], ["t", "h", "e"])
    assert test == True
    
    #Test long word played on start of word - opposite direction
    test = touch_check("the", ["the"], ["there", "h", "e"])
    assert test == True    
    
    #Test long word played on start of word - same direction
    test = touch_check("the", ["there"], ["t", "h", "e"])
    assert test == True
    
    #Test long word played in middle of word
    
    test = touch_check("the", ["the"], ["t", "shore", "e"])
    assert test == True
    
def test_touch_check_short():
    
    #Test single letter not touching
    test = touch_check("a", ["a"], ["a"])
    assert test == False
    
    #Test single letter played on end of word
    test = touch_check("a", ["aha"], ["a"])
    assert test == True
    
    #Test single letter played on start of word
    test = touch_check("a", ["aha"], ["a"])
    assert test == True
    
    #Test single letter played in middle of word
    test = touch_check("h", ["aha"], ["h"])
    assert test == True    
    
    #Test single letter played on side of existing word
    test = touch_check("a", ["ah"], ["a"])
    assert test == True
    
def test_check_word():
    #check_word(word, wordList)  
    wordList = ["the", "them", "there"]
    
    test = check_word("the", wordList)
    assert test == True
    
    test = check_word("this", wordList)
    assert test == False
    
    test = check_word("THEM", wordList)
    assert test == True
    
    
    
    
    
    
    