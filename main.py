# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:37:36 2020

@author: craig
"""

"""
To Do:
    Implement no playing a tile on top of the same letter
    Implement no playing 's' only to pluralize a word
    

This version has the following issues:
    Cannot play around a tile (ie, the second letter was already on the board)
    
"""


#Testing for comment changes
 
import time
import copy

from colorama import Back
from colorama import Style

from classes import tile, player
from checks import initial_checks, touch_check, check_word

from config import MAXHEIGHT, WIDTH, LENGTH, HANDSIZE

clear = "\n" * 100

### Horizontal words have orientation = 1
### Vertical words have orientation = -1

#Get valid words
def create_words():
    """
    Create the list of valid words for a game
    Requires file 'large.txt' to be in same directory
    """
    words = []
    with open('large.txt', 'r') as file:
        for line in file:
            words.append(line.rstrip())
    return words

#Create letter pool
def create_letterpool():
    """Create the letters that can be drawn for the duration of the game"""
        
    letters = []
    for letter in "fjkvwxz":
        letters.append(letter)
    for letter in "bcghry":
        for i in range(2):
            letters.append(letter)   
    for letter in "dlmnpsu":
        for i in range(3):
            letters.append(letter)
    for letter in "iot":
        for i in range(4):
            letters.append(letter)
    for i in range(5):
        letters.append('a')
    for i in range(6):
        letters.append('e')
    letters.append('(qu)')        
    
    return letters

def build_tiles(width, length):
    """
    Create a list of lists, each containing a width's worth of tiles

    Parameters
    ----------
    def build_tiles : TYPE
        DESCRIPTION.

    Returns
    -------
    tiles : TILE
        DESCRIPTION.

    """
    #Build test grid of tiles
    tiles = []

    #Create a list of tiles. 0-8 in row 0, 9-15 in row 1, etc.
    for row in range(width):
        for col in range (length):
            tiles.append(tile(row, col))

    return tiles

"""
These functions are to see what words are played by the user.
make_word takes a starting location and recursivly creates a single word until no more letters
get_words takes the location of the played tiles and assembles all words affected by the played letters 
find_start finds the tile of the first letter in a word
"""
   
def make_word(word, location, orientation, tiles, tile, height):
    """
    Input a starting location and recursivly create a single word until no more letters
    """
    #Checking for a hozontal word
    if orientation == 1:
        #If tile is at the right edge of the board
        if location[1] + 1 == WIDTH:
            
            #Add current letter to word and end
            word = word + tile.get_letter()
            height = height + tile.get_height()
            return word, height
        
        #All other tiles
        for nextTile in tiles:
            
            #If tile is at the end of the word (next letter is a 0)
            if nextTile.get_location() == (location[0], location[1] + 1):
                if nextTile.get_letter() == 0:
                    
                    #Add current letter to word and end
                    word = word + tile.get_letter()
                    height = height + tile.get_height()
                    return word, height
            
            #Not at the end of the word 
                else:
                    #Add current letter and call on next letter
                    word = word + tile.get_letter()
                    height = height + tile.get_height()
                    
                    new_word, new_height = make_word(word, (location[0], location[1] + 1), orientation, tiles, nextTile, height)
                    return new_word, new_height
                    
    
    #Checking for a vertical word
    if orientation == -1:
        
        #If tile is at the bottom of the board
        if location[0] + 1 == LENGTH:
            
            #Add current letter and end
            word = word + tile.get_letter()
            height = height + tile.get_height()
            return word, height
        
        #All other tiles
        for nextTile in tiles:
            
            #If tile is at the end of the word (next letter is a 0)
            if nextTile.get_location() == (location[0] + 1, location[1]):
                if nextTile.get_letter() == 0:
                    
                    #Add current letter and end
                    word = word + tile.get_letter()
                    height = height + tile.get_height()
                    return word, height
                
                #Not at end of word yet
                else:
                    #Add current word and call on next letter in word
                    word = word + tile.get_letter()
                    height = height + tile.get_height()
                    
                    new_word, new_height = make_word(word, (location[0] + 1, location[1]), orientation, tiles, nextTile, height)
                    return new_word, new_height
            
def find_start(word, location, orientation, tiles):
    """
    Given a location and orientation of played tiles, finds the beginning of the word
    If word is played horizontally, will find the location of the leftmost letter
    If word is played vertically, will find the location of the top letter
    
    Outputs the starting tile (type tile)
    """
    
    #For a horizontal word - Look to the left
    if orientation == 1:
        
        #Tile is at far left, so has to be start
        if location[1] == 0:
            for play_tile in tiles:
                if play_tile.get_location() == location:
                    return play_tile     
                
        for prevTile in tiles:
            if prevTile.get_location() == (location[0], location[1] - 1):
    
                #Previous letter is a 0, so current tile is start
                if prevTile.get_letter() == 0:
                    for play_tile in tiles:
                        if play_tile.get_location() == location:
                            return play_tile
                            
                #Previous tile is not 0, so recheck starting at that location         
                else:
                    new_tile = find_start(word, (location[0], location [1] - 1), orientation, tiles)
                    return new_tile
    
    #For a vertical word - Look up                        
    if orientation == -1:  
        
        #Tile is on top row, so has to be start
        if location[0] == 0:
            for play_tile in tiles:
                if play_tile.get_location() == location:
                    return play_tile
        
        for prevTile in tiles:
            if prevTile.get_location() == (location[0] - 1, location[1]):
                
                #Previous letter is a 0, so current tile is start
                if prevTile.get_letter() == 0:
                    for play_tile in tiles:
                        if play_tile.get_location() == location:
                            return play_tile
                        
                #Previous tile is not 0, so recheck starting at that location
                else:
                    new_tile = find_start(word, (location[0] - 1, location[1]), orientation, tiles)
                    return new_tile

                       
def get_words(word, location, orientation, tiles, turn):
    """Based on the letters played, uses make_word to assemble a list of all new words"""
    
    main_word = []
    acc_words = []
    main_height = []
    acc_heights = []
    #startTile = tile(0,0)
    
    #Playing a QU tile currently shortens the word by 1 on the board
    wordLength = len(word)
    if "q" in word:
        wordLength -= 1
    
    #Horizontal word played
    if orientation == 1:
       
        #Get horizontal word
        
        #Check if far left
        if location[1] == 0:
            for play_tile in tiles:
                if play_tile.get_location() == location:
                    startTile = play_tile
                    new_word, new_height = make_word("", location, orientation, tiles, play_tile, 0)
                    main_word.append(new_word)
                    main_height.append(new_height)
        
        #Find the start and build word from there
        else:
            startTile = find_start(word, location, orientation, tiles)
            new_word, new_height = make_word("", startTile.location, orientation, tiles, startTile, 0)
            main_word.append(new_word)
            main_height.append(new_height)
                    
                                 
        #Now check for all vertical words that may be affected by played letters  
        #Check to see if top row
        if location[0] == 0:               
            for i in range(wordLength):
                
                #Check to see if next tile isn't a 0 (a word was actually made)
                for nextTile in tiles:
                    if nextTile.get_location() == (startTile.location[0] + 1, location[1] + i):
                        if nextTile.get_letter() != 0:
                            
                            #Find tile that we're actually reviewing this iteration and create word from start
                            for play_tile in tiles:
                                if play_tile.get_location() == (startTile.location[0], startTile.location[1] + i):                           
                                    new_word, new_height = make_word("", location, orientation * -1, tiles, play_tile, 0)
                                    acc_words.append(new_word)
                                    acc_heights.append(new_height)
                         
        #If word does not start on top row
        else:
            for i in range(wordLength):
                
                #Find start of word for letter we're reviewing, then create word
                nextStart = find_start(word, (location[0], location[1] + i), orientation * -1, tiles)
                new_word, new_height = make_word("", nextStart.location, orientation * -1, tiles, nextStart, 0)
                acc_words.append(new_word)
                acc_heights.append(new_height)
    
    #Vertical word played
    else:
        
        #Check if top row
        if location[0] == 0:
            for play_tile in tiles:
                if play_tile.get_location() == location:
                    startTile = play_tile
                    new_word, new_height = make_word("", location, orientation, tiles, play_tile, 0)
                    main_word.append(new_word)
                    main_height.append(new_height)
                    
        #Find the start and build word from there
        else:
            startTile = find_start(word, location, orientation, tiles)
            new_word, new_height = make_word("", startTile.location, orientation, tiles, startTile, 0)
            main_word.append(new_word)
            main_height.append(new_height)
            
        #Check for all horizontal words that may be affected by played letters
        #Check to see if far left
        if location[1] == 0:
            for i in range(wordLength):
                
                #Check to see if next tile isn't a 0
                for nextTile in tiles:
                    if nextTile.get_location() == (startTile.location[0] + i, location[1] + 1):
                        if nextTile.get_letter() != 0:
                            
                            #Find tile that we're actually reviewing this iteration and create word from start
                            for play_tile in tiles:
                                if play_tile.get_location() == (startTile.location[0] + i, startTile.location[1]):
                                    new_word, new_height = make_word("", location, orientation * -1, tiles, play_tile, 0)
                                    acc_words.append(new_word)
                                    acc_heights.append(new_height)
                                    
        #If word does not start on far left
        else:
            for i in range(wordLength):
                
                #Find start of word for letter we're reviewing then create word
                nextStart = find_start(word, (location[0] + i, location[1]), orientation * -1, tiles)
                new_word, new_height = make_word("", nextStart.location, orientation * -1, tiles, nextStart, 0)
                acc_words.append(new_word)
                acc_heights.append(new_height)
    
    #Check that the tiles were played touching an existing tile
    #Only valid after the first turn
    if turn != 0:
        if touch_check(word, main_word, acc_words):
            #print("Touch Check --- Pass")
            words = main_word + acc_words
            heights = main_height + acc_heights
            touch = True
        else:
           # print("ERROR --- Not Touching!")
            words = main_word + acc_words
            heights = main_height + acc_heights
            touch = False
    else:
        touch = True
        words = main_word + acc_words
        heights = main_height + acc_heights
    
    #Remove any single letter words (or QU)
    words_copy = words.copy()
    heights_copy = heights.copy()
    for i in range(len(words)):
        if len(words[i]) == 1 or words[i] == "qu":
            words_copy.remove(words[i])
            heights_copy.remove(heights[i])
    
    return words_copy, heights_copy, touch    

        
def score_word(word, height):
    """Get score of a word"""
    
    wordScore = 0
    
    #If QU tile is in word
    score_word_len = len(word)
    if "q" in word:
        score_word_len -= 1
    
    if score_word_len / height == 1:  #If height of all tiles is 1
        wordScore += 2*score_word_len
        
        #Bonus 2 points if QU is used a word of all height 1 tiles
        if "q" in word:
            wordScore += 2
        
    else:
        wordScore = height
    
    #If user plays all 7 tiles in their hand
    # if len(hand = 0):
    #     wordScore += 20
        
    return wordScore 

def update_score_end(players):
    """Remove 5 points for every letter in a player's hand at end of game"""
    
    for name in players:
        for letter in name.get_hand():
            name.update_score(-5)
    
    return None
    
   
 
def update_board(word, tiles, orientation, location):
    """Update the board with the played tiles"""
    
    
    """Need to figure out how to apply QU to this"""
    
    word_copy = word
    
    #If QU was played, remove the 'u' from the word
    if "q" in word_copy:
        for spot_search in range(len(word_copy)):
            if word_copy[spot_search] == "q":
                spot = spot_search
                
        word_copy = word_copy[:spot + 1] + word_copy[spot + 2:]
    
    
    #Iterate through the word and update each tile
    for i in range(len(word_copy)):
        
        #Horizontal word
        if orientation == 1:
            #Find tile and update letter
            for play_tile in tiles:
                if play_tile.get_location() == (location[0], location[1] + i):
                    #If qu tile is played, need those letters on the board together, and no 'u' after
                    if word_copy[i] == "q":
                        play_tile.update_letter("qu")
                        play_tile.update_height()
                    
                    else:
                        play_tile.update_letter(word_copy[i])
                        play_tile.update_height()
                        play_tile.check_valid()
                    
        
        #Vertical word            
        else:
            #Find tile and update letter
            for play_tile in tiles:
                if play_tile.get_location() == (location[0] + i, location[1]):
                    
                    if word_copy[i] == "q":
                        play_tile.update_letter("qu")
                        play_tile.update_height()
                        
                    else:
                        play_tile.update_letter(word_copy[i])
                        play_tile.update_height()
                        play_tile.check_valid()
    
#Show the updated grid
def print_grid(tiles):
    """Show the letters on the grid"""
    print("Heights")
    print(f"{Back.GREEN}1 {Back.CYAN}2 {Back.BLUE}3 {Back.YELLOW}4 {Back.RED}5 {Style.RESET_ALL}")
    print()
  
    for row in range(LENGTH):
        row_print = []
        height_print = []
        for play_tile in tiles:
            if play_tile.get_location()[0] == row:
                if play_tile.get_letter() != 0:
                    row_print.append(play_tile.get_letter())
                    height_print.append(play_tile.get_height())
                else:
                    row_print.append("-")
                    height_print.append(0)
        
        for letter in range(len(row_print)):
            value = row_print[letter]
            height = height_print[letter]
            
            if height == 0:
                print("%-3s" %value, end = "" )
            elif height == 1:
                print(f"{Back.GREEN}%-3s{Style.RESET_ALL}" %value, end = "")
            elif height == 2:
                print(f"{Back.CYAN}%-3s{Style.RESET_ALL}" %value, end = "")                
            elif height == 3:
                print(f"{Back.BLUE}%-3s{Style.RESET_ALL}" %value, end = "")
            elif height == 4:
                print(f"{Back.YELLOW}%-3s{Style.RESET_ALL}" %value, end = "")
            else:
                print(f"{Back.RED}%-3s{Style.RESET_ALL}" %value, end = "")
        
        print()
            
    return None

def play_word(wordList, letters, tiles, player, word, turn):
    """
    The majority of the user interaction in a turn. Player chooses a location to play their new word and the direction of the word
    Creates a copy of the board and checks for the following:
        User has the tiles in their hand
        Word fits on the board
        All tiles can be played on
        All words played exist
        Tiles are played in a valid location
        
    Once all tests are passed, marked as True and all words are scored. The players hand is then filled with
    tiles (assuming they are available)
    
    Inputs: wordList (list of valid words (strings)), letters (list of letters (length 1 string) remaining in the 'bag')
            tiles (list of type tile for each square on the board), player (who's turn it is), word (string, tiles played by player)
            turn (how many turns have passed)
            
    Outputs: Updates set of tiles
    
    """
    
    turn_tiles = copy.deepcopy(tiles)
    turn_checks = False
    
    while turn_checks == False:        
        location = (input("What location would you like to play at? "))
        location = (int(location[0]), int(location[1]))
        orientation = input("Would you like this to be vertical or horizontal (v/h)? ")
        if orientation == "h":
            orientation = 1       
        else:
            orientation = -1
         
        
        #Check word played 
        update_board(word, turn_tiles, orientation, location)
        
        #Find affected words
        words, heights, touch = get_words(word, location, orientation, turn_tiles, turn)
        print("The played words were: ")
        for j in range(len(words)):
            print(words[j], " - ", heights[j])
        print()
        print("The new board is:")
        print()
        print_grid(turn_tiles)
        print()
               
        #Check words affected    
        print()
        print("Checking to see if all words are valid...")
        for j in range(len(words)):
            real_words = check_word(words[j], wordList)
            initial = initial_checks(word, player.get_hand(), location, orientation, turn_tiles)
            if touch:
                print("Touch Check --- Pass")
            else:
                print("ERROR --- Not Touching!")
            print()
                    
        #Ensure that the turn is allowed
        if not initial or not real_words or not touch:
            print("This is not a legal move! Try again")
            print()
            print("Here is the board")
            print_grid(tiles)
            
            print("Here is your hand:", player.get_hand())
            word = input("What would you like to play? ")
                        
            print()
            
        else:
            turn_checks = True
            
            
    #Score turn    
    print()
    print("Getting turn score...")
    turn_score = 0
    for j in range(len(words)):
        turn_score += score_word(words[j], heights[j])
        
    if len(word) == 7:
        print("WOW! You played your entire hand! Bonus 20 points!")
        turn_score += 20
                
    player.update_score(turn_score)
    print("You scored", turn_score, "points this turn!")
    print("You have", player.get_score(), "points!")
    time.sleep(3)
    print()
    #print(clear)
    
    
    #Update player's hand
    for j in word:
        player.remove_letter(player.get_hand(), j)
        
    player.update_hand(player.get_hand(), letters)
    
    
    
    tiles = copy.deepcopy(turn_tiles)
    return tiles

def exchange_tile(player, letters):
    """
    The player can trade in one letter for another from the bag as their turn
    Ensures that only one letter is exchanged, and that the player has that letter in their hand
    Removes the chosen letter from the user's hand and adds a random remaining letter to the player's hand
    Adds the chosen letter back into the letter pool
    """
    
    print("Here is your hand:", player.get_hand())
    letter = input("What letter would you like to exchange? ")
    
    exchange_go = False
    while exchange_go == False:

        #Ensure user inputted a single letter
        if len(letter) == 1 or letter == "(qu)":
            #Ensure the player had that letter in their hand
            if letter in player.get_hand():        
                player.remove_letter(player.get_hand(), letter)
                player.update_hand(player.get_hand(), letters)
                letters.append(letter)
                exchange_go = True
            else:
                print("You must choose a letter in your hand!")  
                print()
                print("Here is your hand:", player.get_hand())
                letter = input("What letter would you like to exchange? ")
        else:
            print("You can only exchange one letter!")
            print()
            print("Here is your hand:", player.get_hand())
            letter = input("What letter would you like to exchange? ")  
            
def print_final_scores(players):
    """Print out a table of players in order of highest score"""
    
    score_sorted_players = []
    players_copy = players.copy()

    #Sort through the copied list until all players have been moved to the sorted list
    while len(players_copy) > 0:    
        #Iterate through the players to see who has the highest score
        highest = 0
        for i in range(len(players_copy)):
            
            if players_copy[i].get_score() > highest:
                highest = players_copy[i].get_score()
                top_player = i
                
        #Add top player to sorted list and remove from player copy
        score_sorted_players.append(players_copy[top_player])
        del players_copy[top_player]


    print("%-6s %-10s %s" %("Rank", "Name", "Score"))
    for i in range(len(players)):
        print("%-6s %-10s %i" %(i + 1, score_sorted_players[i].get_name(), score_sorted_players[i].get_score()))
            

#Play the game
def play_game(wordList, letters, tiles):
    """
    Executes the game. Allows the user to create players, then loops through turns until game is complete.
    Once game is complete, prints out a list of players and their rank & score

    Parameters
    ----------
    wordList : List of strings
        All the playable words in the game
    letters : List of letters
        Letters that remain in the 'bag' - at beginning of game = all letters
    tiles : List of tiles
        The board upon which letters are played. List of lists, each containing WIDTH tiles
        tiles [y][x] returns the tile at location (x,y)

    Returns
    -------
    None.

    """

    turn = 0
    
    print("Here is the game board")
    print()
    print_grid(tiles)
    print()
    
    playernum = int(input("How many players? "))
    print()
    
    #Create the players for the game
    players = []
    for i in range(playernum):
        print("Creating Player ", i + 1)
        name = input("What is the name of the player? ")
        players.append(player(name, "", 0, i))
        players[i].update_hand("", letters)
        print()

    passing_players = 0            
  
    #Turns
    print("Beginning the game")
    play_turns = True
    while play_turns == True:
        
        #Checking to ensure letters are running out
        #print("There are", len(letters), "tiles left")
        
        for i in range(playernum):
            #Start turn, get letters to play
            print("Player", players[i].get_name(), "it is your turn.")
            print("Here is your hand:", players[i].get_hand())
            print()
            print_grid(tiles)
            print()
             
            #Give player option to pass their turn
            turn_go = False
            while turn_go == False:
                print("You can pass your turn by inputting PASS as your word (case sensitive)")
                print("You can exchange a letter in your hand by inputting EXCHANGE as your word")
                word = input("What word would you like to play? ")
         
                if word != "PASS" and word != "EXCHANGE":
                    passing_players = 0
                    turn_go = True
                    word = word.lower()
                    tiles = play_word(wordList, letters, tiles, players[i], word, turn)
                    
                elif word == "EXCHANGE":
                    
                    excCheck = input("Are you sure? (y/n) ")
                    if excCheck == 'y':
                        print()
                        exchange_tile(players[i], letters)
                        passing_players = 0
                        turn_go = True
                    else:
                        print()
                        print("Here is your hand:", players[i].get_hand())
                        print()
                        print_grid(tiles)
                        print()
                        
                #User inputted "PASS"
                else:
                    passCheck = input("Are you sure? (y/n) ")
                    if passCheck == 'y':
                        print()
                        passing_players += 1
                        
                        #If board is blank, don't want to throw off touch check
                        if turn == 0:
                            turn = -1
                            
                        turn_go = True
                    else:
                        print()
                        print("Here is your hand:", players[i].get_hand())
                        print()
                        print_grid(tiles)
                        print()
                           
            turn += 1
            
            #All players in a row passed in a row
            if passing_players == len(players):
                print("All players have passed! The game is now over.")
                print()
                play_turns = False
                break
            
            if len(players[i].get_hand()) == 0 & len(letters) == 0:
                play_turns = False
                
            
            
    #End the game
    print("GAME OVER")

    update_score_end(players)
    print_final_scores(players)        

"""
Testing
"""

#play_game(create_words(), create_letterpool(), build_tiles(WIDTH, LENGTH))

#print_grid(tiles)

# #Test One
# print("Test One")
# orientation = 1
# word = "three"
# hand = "threeoi"
# location = (0,0)

# initial_checks(word, hand, location, orientation, tiles)
# check_word(word, wordList)
# print()

# #Test Two
# print("Test Two")
# location = (6,0)
# check_location(word, location, orientation)
# print()
