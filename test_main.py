# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:30:10 2020

@author: craig
"""


from classes import player, tile
from main import create_words, create_letterpool, build_tiles, make_word

def test_create_words():
    assert len(create_words()[0]) == 1
    assert len(create_words()) == 143091 #If failing, check if dictionary was changed
    
def test_create_letterpool():
    letters = create_letterpool()
    assert len(letters) == 64
    assert len(letters[0]) == 1
    assert len(letters[63]) == 4 #(qu))
    
def test_build_tiles():
    tiles = build_tiles(8, 8)
    assert len(tiles) == 64
    assert type(tiles[0]) == tile
    assert tiles[0].get_location() == (0,0)
    assert tiles[8].get_location() == (1,0)
    assert tiles[63].get_location() == (7,7)
    
    tiles = build_tiles(5,10)
    assert len(tiles) == 50
    
def test_make_word_hor():
    tiles = build_tiles(8,8)
    
    #Test generic horizontal word - Update Board
    tiles[11].update_letter('t')
    for i in range(2):
        tiles[11].update_height()   
    tiles[12].update_letter('h')
    tiles[12].update_height()
    tiles[13].update_letter('e')
    tiles[13].update_height()
    
    #Recall that make_word requires the starting location of the word
    word, height = make_word('', tiles[11].get_location(), 1, tiles, tiles[11], 0)
    assert type(word) == str
    assert type(height) == int
    assert word == 'the'
    assert height == 4
    
    #Test horizontal word that starts at left edge
    tiles[8].update_letter('h')
    tiles[8].update_height()
    tiles[9].update_letter('i')
    tiles[9].update_height()
    
    word, height = make_word('', tiles[8].get_location(), 1, tiles, tiles[8], 0)
    assert type(word) == str
    assert type(height) == int
    assert word == 'hi'
    assert height == 2    
    
    #Test horizontal word that ends at right edge
    tiles[14].update_letter('r')
    tiles[14].update_height()
    tiles[15].update_letter('e')
    tiles[15].update_height()
 
    word, height = make_word('', tiles[11].get_location(), 1, tiles, tiles[11], 0)
    assert type(word) == str
    assert type(height) == int
    assert word == 'there'
    assert height == 6
    
    #Test word going across entire board
    tiles[10].update_letter('qu')
    tiles[10].update_height()
    
    word, height = make_word('', tiles[8].get_location(), 1, tiles, tiles[8], 0)
    assert type(word) == str
    assert type(height) == int
    assert word == 'hiquthere'
    assert height == 9
    
    #Test single letter
    tiles[26].update_letter('t')
    tiles[26].update_height()
    
    word, height = make_word('', tiles[26].get_location(), 1, tiles, tiles[26], 0)
    assert word == 't'
    assert height == 1

def test_make_words_vert():
    tiles = build_tiles(8,8)

    #Test generic vertical word

    #Test word that starts on top row

    #Test word that ends on bottom row

    #Test word that goes across entire board

    #Test single letter    




