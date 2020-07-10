# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:30:10 2020

@author: craig
"""


from classes import player, tile
from main import create_words, create_letterpool, build_tiles, make_word
from main import find_start, get_words, score_word, update_score_end
from main import update_board, exchange_tile

#Slowest test by a lot - uncomment if you want to run
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
    
def test_get_words_middle_hor():
    #Includes middle word with no accessory words
    tiles = build_tiles(8,8)
    
    #Test single word
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[12].update_letter('h')
    tiles[12].update_height()
    tiles[13].update_letter('e')
    tiles[13].update_height()
    
    words, heights, touch = get_words('the', (1, 3), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'the'
    assert len(heights) == 1
    assert heights[0] == 3    
    
    #Test word with middle word up
    tiles[4].update_letter('o')
    tiles[4].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'oh'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2
    
    #Test word with middle word down    
    tiles[4].update_letter(0)
    tiles[20].update_letter('i')
    tiles[20].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'hi'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2    
    
    #Test word with middle word both up and down
    tiles[4].update_letter('o')
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ohi'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3   

def test_get_words_start_hor():
    tiles = build_tiles(8,8)
    
    #Create board
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[12].update_letter('h')
    tiles[12].update_height()
    tiles[13].update_letter('e')
    tiles[13].update_height()        
    
    #Test word with start word up    
    tiles[3].update_letter('a')
    tiles[3].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'at'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2 
    
    #Test word with start word down
    tiles[3].update_letter(0)   
    tiles[19].update_letter('o')
    tiles[19].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'to'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2     
    
    #Test word with start word up and down
    tiles[3].update_letter('a')
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ato'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3   

def test_get_word_end_hor():
    tiles = build_tiles(8,8)
    
    #Create board
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[12].update_letter('h')
    tiles[12].update_height()
    tiles[13].update_letter('e')
    tiles[13].update_height()     
    
    #Test word with end word up
    tiles[5].update_letter('h')
    tiles[5].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'he'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2    
    
    #Test word with end word down
    tiles[5].update_letter(0)
    tiles[21].update_letter('h')
    tiles[21].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'eh'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2     
    
    #Test word with end word up and down
    tiles[5].update_letter('h')
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'heh'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3

def test_get_words_multiple_hor():
    tiles = build_tiles(8,8)
    
    #Test single word
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[12].update_letter('h')
    tiles[12].update_height()
    tiles[13].update_letter('e')
    tiles[13].update_height()   
    tiles[5].update_letter('h')
    tiles[5].update_height()
    tiles[21].update_letter('h')
    tiles[21].update_height()
    
    #Test word with multiple accessory words
    tiles[3].update_letter('a')
    tiles[3].update_height()
    tiles[19].update_letter('o')
    tiles[19].update_height()
    
    words, heights, touch = get_words('the', (1,3), 1, tiles, 0)
    assert len(words) == 3
    assert words[0] == 'the'
    assert words[1] == 'ato'
    assert words[2] == 'heh'
    assert len(heights) == 3
    assert heights[0] == 3
    assert heights[1] == 3 
    assert heights[2] == 3    
    
def test_get_words_top():    
    #Test word on top row
    tiles = build_tiles(8,8)

    tiles[2].update_letter('t')
    tiles[2].update_height()
    tiles[3].update_letter('h')
    tiles[3].update_height()
    tiles[4].update_letter('e')
    tiles[4].update_height()
    tiles[12].update_letter('l')
    tiles[12].update_height()
    tiles[20].update_letter('f')
    tiles[20].update_height() 
    
    words, heights, touch = get_words('the', (0,2), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'elf'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3  
    
def test_get_words_bottom():
    tiles = build_tiles(8,8)
    
    #Test word on bottom row
    tiles[58].update_letter('t')
    tiles[58].update_height()
    tiles[59].update_letter('h')
    tiles[59].update_height()
    tiles[60].update_letter('e')
    tiles[60].update_height()
    tiles[44].update_letter('t')
    tiles[44].update_height()
    tiles[52].update_letter('h')
    tiles[52].update_height()   
    
    words, heights, touch = get_words('the', (7,2), 1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'the'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3      

def test_get_words_adding_hor():  
    #Test adding on to start of a blank word
    tiles = build_tiles(8,8)    
    tiles[17].update_letter('t')
    tiles[17].update_height()
    tiles[18].update_letter('h')
    tiles[18].update_height()
    tiles[19].update_letter('e')
    tiles[19].update_height()
    tiles[20].update_letter('r')
    tiles[20].update_height()
    tiles[21].update_letter('e')
    tiles[21].update_height()
    
    words, heights, touch = get_words('t', (2,1), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5    
        
    #Test adding on to start of a word with cross words
    tiles[11].update_letter('e')
    tiles[11].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()
    
    words, heights, touch = get_words('t', (2,1), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5      
    
    #Test adding on to end of a blank word
    tiles = build_tiles(8,8)
    
    tiles[17].update_letter('t')
    tiles[17].update_height()
    tiles[18].update_letter('h')
    tiles[18].update_height()
    tiles[19].update_letter('e')
    tiles[19].update_height()
    tiles[20].update_letter('r')
    tiles[20].update_height()
    tiles[21].update_letter('e')
    tiles[21].update_height()    

    words, heights, touch = get_words('e', (2,5), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5 
    
    #Test adding on to end of a word with cross words
    tiles[11].update_letter('e')
    tiles[11].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()
   
    words, heights, touch = get_words('e', (2,5), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
  
def test_get_words_diagonals_hor():
    #Test letter diagonal top left
    tiles = build_tiles(8,8)
    
    tiles[17].update_letter('t')
    tiles[17].update_height()
    tiles[18].update_letter('h')
    tiles[18].update_height()
    tiles[19].update_letter('e')
    tiles[19].update_height()
    tiles[20].update_letter('r')
    tiles[20].update_height()
    tiles[21].update_letter('e')
    tiles[21].update_height()
    tiles[8].update_letter('h')
    tiles[8].update_height()

    words, heights, touch = get_words('there', (2,1), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
    
    #Test letter diagonal top right
    tiles[14].update_letter('h')
    tiles[14].update_height()

    words, heights, touch = get_words('there', (2,1), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
    
    
    #Test letter diagonal bottom left
    tiles[24].update_letter('h')
    tiles[24].update_height()

    words, heights, touch = get_words('there', (2,1), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
    
    
    #Test letter diagonal bottom right
    tiles[30].update_letter('h')
    tiles[30].update_height()

    words, heights, touch = get_words('there', (2,1), 1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5
    
def test_get_words_middle_vert():    
    #Includes middle word with no accessory words
    tiles = build_tiles(8,8)
    
    #Test single word
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()
    
    words, heights, touch = get_words('the', (1, 3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'the'
    assert len(heights) == 1
    assert heights[0] == 3    
    
    #Test word with middle word right
    tiles[20].update_letter('o')
    tiles[20].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ho'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2
    
    #Test word with middle word left    
    tiles[20].update_letter(0)
    tiles[18].update_letter('i')
    tiles[18].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ih'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2    
    
    #Test word with middle word both right and left
    tiles[20].update_letter('o')
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'iho'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3       
    
def test_get_words_start_vert():
    tiles = build_tiles(8,8)
    
    #Create board
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()        
    
    #Test word with start word right
    tiles[12].update_letter('a')
    tiles[12].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ta'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2 
    
    #Test word with start word left
    tiles[12].update_letter(0)   
    tiles[10].update_letter('o')
    tiles[10].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ot'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2     
    
    #Test word with start word right and left
    tiles[12].update_letter('a')
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'ota'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3
    
def test_get_words_end_vert():
    tiles = build_tiles(8,8)
    
    #Create board
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()     
    
    #Test word with end word right
    tiles[28].update_letter('h')
    tiles[28].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'eh'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2    
    
    #Test word with end word left
    tiles[28].update_letter(0)
    tiles[26].update_letter('h')
    tiles[26].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'he'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 2     
    
    #Test word with end word right and left
    tiles[28].update_letter('h')
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'heh'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3
    
def test_get_words_multiple_vert():
    tiles = build_tiles(8,8)
    
    #Test single word
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()   
    tiles[26].update_letter('h')
    tiles[26].update_height()
    tiles[28].update_letter('h')
    tiles[28].update_height()
    
    #Test word with multiple accessory words
    tiles[10].update_letter('a')
    tiles[10].update_height()
    tiles[12].update_letter('o')
    tiles[12].update_height()
    
    words, heights, touch = get_words('the', (1,3), -1, tiles, 0)
    assert len(words) == 3
    assert words[0] == 'the'
    assert words[1] == 'ato'
    assert words[2] == 'heh'
    assert len(heights) == 3
    assert heights[0] == 3
    assert heights[1] == 3 
    assert heights[2] == 3

def test_get_words_left():
    #Test word on left edge
    tiles = build_tiles(8,8)

    tiles[8].update_letter('t')
    tiles[8].update_height()
    tiles[16].update_letter('h')
    tiles[16].update_height()
    tiles[24].update_letter('e')
    tiles[24].update_height()
    tiles[25].update_letter('l')
    tiles[25].update_height()
    tiles[26].update_letter('f')
    tiles[26].update_height() 
    
    words, heights, touch = get_words('the', (1,0), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'elf'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3   

def test_get_words_right():
    tiles = build_tiles(8,8)
    
    #Test word on bottom row
    tiles[15].update_letter('t')
    tiles[15].update_height()
    tiles[23].update_letter('h')
    tiles[23].update_height()
    tiles[31].update_letter('e')
    tiles[31].update_height()
    tiles[13].update_letter('t')
    tiles[13].update_height()
    tiles[14].update_letter('h')
    tiles[14].update_height()   
    
    words, heights, touch = get_words('the', (1,7), -1, tiles, 0)
    assert len(words) == 2
    assert words[0] == 'the'
    assert words[1] == 'tht'
    assert len(heights) == 2
    assert heights[0] == 3
    assert heights[1] == 3 

def test_get_words_adding_vert():
    #Test adding on to start of a blank word
    tiles = build_tiles(8,8)    
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()
    tiles[35].update_letter('r')
    tiles[35].update_height()
    tiles[43].update_letter('e')
    tiles[43].update_height()
    
    words, heights, touch = get_words('t', (1,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5    
        
    #Test adding on to start of a word with cross words
    tiles[26].update_letter('e')
    tiles[26].update_height()
    tiles[28].update_letter('e')
    tiles[28].update_height()
    
    words, heights, touch = get_words('t', (1,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5      
    
    #Test adding on to end of a blank word
    tiles = build_tiles(8,8)
        
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()
    tiles[35].update_letter('r')
    tiles[35].update_height()
    tiles[43].update_letter('e')
    tiles[43].update_height()   

    words, heights, touch = get_words('e', (5,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5 
    
    #Test adding on to end of a word with cross words
    tiles[26].update_letter('e')
    tiles[26].update_height()
    tiles[28].update_letter('e')
    tiles[28].update_height()
   
    words, heights, touch = get_words('e', (5,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5    
    
def test_get_words_diagonal_vert():
    #Test letter diagonal top left
    tiles = build_tiles(8,8)
    
    tiles[11].update_letter('t')
    tiles[11].update_height()
    tiles[19].update_letter('h')
    tiles[19].update_height()
    tiles[27].update_letter('e')
    tiles[27].update_height()
    tiles[35].update_letter('r')
    tiles[35].update_height()
    tiles[43].update_letter('e')
    tiles[43].update_height()  
    tiles[2].update_letter('h')
    tiles[2].update_height()

    words, heights, touch = get_words('there', (1,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
    
    #Test letter diagonal top right
    tiles[4].update_letter('h')
    tiles[4].update_height()

    words, heights, touch = get_words('there', (1,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
    
    
    #Test letter diagonal bottom left
    tiles[50].update_letter('h')
    tiles[50].update_height()

    words, heights, touch = get_words('there', (1,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5     
    
    
    #Test letter diagonal bottom right
    tiles[52].update_letter('h')
    tiles[52].update_height()

    words, heights, touch = get_words('there', (1,3), -1, tiles, 0)
    assert len(words) == 1
    assert words[0] == 'there'
    assert len(heights) == 1
    assert heights[0] == 5    

def test_score_word():
    
    score = score_word("hello", 5)
    assert score == 10
    
    score = score_word("hello", 6)
    assert score == 6
    
    score = score_word("queen", 4)
    assert score == 10
    
    score = score_word("queen", 6)
    assert score == 6
    
def test_update_score_end():
    p1 = player("p1", "", 50, 1)
    p2 = player("p2", "abc", 50, 2)
    p3 = player("p3", "(qu)werty", 75, 3)    
    players = [p1, p2, p3]
    
    update_score_end(players)
    
    assert p1.get_score() == 50
    assert p2.get_score() == 35
    assert p3.get_score() == 45
    
def test_update_board_middle_hor():
    tiles = build_tiles(8,8)
    
    #Horizontal word in middle of board
    update_board("the", tiles, 1, (1,3))
    assert tiles[10].get_letter() == 0
    assert tiles[11].get_letter() == 't'
    assert tiles[13].get_letter() == 'e'
    assert tiles[14].get_letter() == 0
    
    assert tiles[10].get_height() == 0
    assert tiles[11].get_height() == 1
    assert tiles[13].get_height() == 1
    assert tiles[14].get_height() == 0
    
    #Horizontal word overwriting existing tiles
    update_board("s", tiles, 1, (1,3))
    assert tiles[10].get_letter() == 0
    assert tiles[10].get_height() == 0
    assert tiles[11].get_letter() == 's'
    assert tiles[11].get_height() == 2
    assert tiles[12].get_letter() == 'h'
    assert tiles[12].get_height() == 1
    
def test_update_board_edges_hor():
    tiles = build_tiles(8,8)
    
    #Horizontal word on top edge
    update_board("the", tiles, 1, (0,2))
    assert tiles[1].get_letter() == 0
    assert tiles[2].get_letter() == 't'
    assert tiles[4].get_letter() == 'e'
    assert tiles[5].get_letter() == 0
    
    assert tiles[1].get_height() == 0
    assert tiles[2].get_height() == 1
    assert tiles[4].get_height() == 1
    assert tiles[5].get_height() == 0
    
    #Horizontal word on bottom edge
    update_board("the", tiles, 1, (7,2))
    assert tiles[57].get_letter() == 0
    assert tiles[58].get_letter() == 't'
    assert tiles[60].get_letter() == 'e'
    assert tiles[61].get_letter() == 0
    
    assert tiles[57].get_height() == 0
    assert tiles[58].get_height() == 1
    assert tiles[60].get_height() == 1
    assert tiles[61].get_height() == 0 
    
    #Horizontal word ending on right edge
    update_board("the", tiles, 1, (3,5))
    assert tiles[28].get_letter() == 0
    assert tiles[29].get_letter() == 't'
    assert tiles[31].get_letter() == 'e'
    
    assert tiles[28].get_height() == 0
    assert tiles[29].get_height() == 1
    assert tiles[31].get_height() == 1
      
    #Horizontal word starting on left edge
    update_board("the", tiles, 1, (2,0))
    assert tiles[16].get_letter() == 't'
    assert tiles[18].get_letter() == 'e'
    assert tiles[19].get_letter() == 0
    
    assert tiles[16].get_height() == 1
    assert tiles[18].get_height() == 1
    assert tiles[19].get_height() == 0 
    
def test_update_board_middle_vert():
    tiles = build_tiles(8,8)
    
    #Vertical word in middle of board
    update_board("the", tiles, -1, (1,3))
    assert tiles[3].get_letter() == 0
    assert tiles[11].get_letter() == 't'
    assert tiles[27].get_letter() == 'e'
    assert tiles[35].get_letter() == 0
    
    assert tiles[3].get_height() == 0
    assert tiles[11].get_height() == 1
    assert tiles[27].get_height() == 1
    assert tiles[35].get_height() == 0
    
    #Vertical word overwriting existing tiles
    update_board("s", tiles, -1, (1,3))
    assert tiles[3].get_letter() == 0
    assert tiles[3].get_height() == 0
    assert tiles[11].get_letter() == 's'
    assert tiles[11].get_height() == 2
    assert tiles[19].get_letter() == 'h'
    assert tiles[19].get_height() == 1
    
def test_update_board_edges_vert():
    tiles = build_tiles(8,8)
    
    #Vertical word on left edge
    update_board("the", tiles, -1, (3,0))
    assert tiles[16].get_letter() == 0
    assert tiles[24].get_letter() == 't'
    assert tiles[40].get_letter() == 'e'
    assert tiles[48].get_letter() == 0
    
    assert tiles[16].get_height() == 0
    assert tiles[24].get_height() == 1
    assert tiles[40].get_height() == 1
    assert tiles[48].get_height() == 0
    
    #Vertical word on right edge
    update_board("the", tiles, -1, (2,7))
    assert tiles[15].get_letter() == 0
    assert tiles[23].get_letter() == 't'
    assert tiles[39].get_letter() == 'e'
    assert tiles[47].get_letter() == 0
    
    assert tiles[15].get_height() == 0
    assert tiles[23].get_height() == 1
    assert tiles[39].get_height() == 1
    assert tiles[47].get_height() == 0 
    
    #Vertical word ending on bottom edge
    update_board("the", tiles, -1, (5,4))
    assert tiles[36].get_letter() == 0
    assert tiles[44].get_letter() == 't'
    assert tiles[60].get_letter() == 'e'
    
    assert tiles[36].get_height() == 0
    assert tiles[44].get_height() == 1
    assert tiles[60].get_height() == 1
      
    #Vertical word starting on top edge
    update_board("the", tiles, -1, (0,5))
    assert tiles[5].get_letter() == 't'
    assert tiles[21].get_letter() == 'e'
    assert tiles[29].get_letter() == 0
    
    assert tiles[5].get_height() == 1
    assert tiles[21].get_height() == 1
    assert tiles[29].get_height() == 0     
    
def test_exchange_tile():
    p1 = player("p1", "abcdefg", 0, 1)
    p2 = player("p2", "abc(qu)fg", 0, 1)
    letters = ["w"]    
    
    exchange_tile(p1, letters, True, "a")
    assert len(letters) == 1
    assert letters[0] == "a"
    assert len(p1.get_hand()) == 7
    assert p1.get_hand() == "bcdefgw"
    
    exchange_tile(p2, letters, True, "(qu)")
    assert len(letters) == 1
    assert letters[0] == "(qu)"
    assert len(p2.get_hand()) == 6
    assert p2.get_hand() == "abcfga"    
    
    
    
    
    
    
    
    