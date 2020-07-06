# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:30:10 2020

@author: craig
"""


from classes import player, tile
from main import create_words, create_letterpool, build_tiles, make_word
from main import find_start

#Slowest test by a lot - uncomment if you want to run
#def test_create_words():
#    assert len(create_words()[0]) == 1
#    assert len(create_words()) == 143091 #If failing, check if dictionary was changed
    
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
    tiles[9].update_letter('t')
    tiles[9].update_height()
    tiles[17].update_letter('h')
    tiles[17].update_height()
    tiles[25].update_letter('e')
    tiles[25].update_height()
    
    word, height = make_word('', tiles[9].get_location(), -1, tiles, tiles[9],0)
    assert type(word) == str
    assert type(height) == int
    assert word == "the"
    assert height == 3

    #Test word that starts on top row
    tiles[1].update_letter('o')
    tiles[1].update_height()
    
    word, height = make_word('', tiles[1].get_location(), -1, tiles, tiles[1],0)
    assert word == "othe"
    assert height == 4

    #Test word that ends on bottom row
    tiles[41].update_letter('i')
    tiles[41].update_height()
    tiles[49].update_letter('n')
    tiles[49].update_height()
    tiles[57].update_letter('o')
    tiles[57].update_height()
    
    word, height = make_word('', tiles[41].get_location(), -1, tiles, tiles[41],0)
    assert word == "ino"
    assert height == 3

    #Test word that goes across entire board
    tiles[33].update_letter('r')
    tiles[33].update_height()
    
    word, height = make_word('', tiles[1].get_location(), -1, tiles, tiles[1],0)
    assert word == "otherino"
    assert height == 8

    #Test single letter
    tiles[51].update_letter('t')
    tiles[51].update_height()
    
    word, height = make_word('', tiles[51].get_location(), -1, tiles, tiles[51],0)
    assert word == 't'
    assert height == 1
    
def test_find_start_hor():
    tiles = build_tiles(8,8)
    
    #Test word in middle of board from start of word
    tiles[11].update_letter('t')
    tiles[12].update_letter('h')
    tiles[13].update_letter('e')

    test_tile = find_start('', tiles[11].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[11].get_location()
    
    #Test word in middle of board from middle of word
    test_tile = find_start('', tiles[12].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[11].get_location()
    
    #Test word in middle of board from end of word
    test_tile = find_start('', tiles[13].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[11].get_location()
    
    #Test word on left side of board from start of word
    tiles[24].update_letter('r')
    tiles[25].update_letter('e')
    tiles[26].update_letter('s')
    tiles[27].update_letter('t')

    test_tile = find_start('', tiles[24].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[24].get_location()
    
    #Test word on left side of board from middle of word
    test_tile = find_start('', tiles[25].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[24].get_location()
    
    #Test word on left side of board from end of word
    test_tile = find_start('', tiles[27].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[24].get_location()
    
    #Test word ending on right side of board from end
    tiles[44].update_letter('r')
    tiles[45].update_letter('e')
    tiles[46].update_letter('s')
    tiles[47].update_letter('t')    

    test_tile = find_start('', tiles[47].get_location(), 1, tiles)
    assert test_tile.get_location() == tiles[44].get_location()
    
def test_find_start_vert():
    tiles = build_tiles(8,8)

    #Check word in middle of board from start of word
    tiles[9].update_letter('t')
    tiles[17].update_letter('h')
    tiles[25].update_letter('e')
    
    test_tile = find_start('', tiles[9].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[9].get_location()
    
    #Check word in middle of board from middle of word
    test_tile = find_start('', tiles[17].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[9].get_location()
    
    #Check word in middle of board from end of word
    test_tile = find_start('', tiles[25].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[9].get_location()
    
    #Check word starting in top row from start of word
    tiles[3].update_letter('t')
    tiles[11].update_letter('h')
    tiles[19].update_letter('e')
    
    test_tile = find_start('', tiles[3].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[3].get_location()
    
    
    #Check word starting in top row from middle of word    
    test_tile = find_start('', tiles[11].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[3].get_location()
    
    #Check word starting in top row from end of word
    test_tile = find_start('', tiles[19].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[3].get_location()
    
    #Check word ending on bottom row from end of word
    tiles[44].update_letter('t')
    tiles[52].update_letter('h')
    tiles[60].update_letter('e')
    
    test_tile = find_start('', tiles[60].get_location(), -1, tiles)
    assert test_tile.get_location() == tiles[44].get_location()
    
def test_get_words_hor():
    



