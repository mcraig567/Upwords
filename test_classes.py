# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 12:59:40 2020

@author: craig
"""

from classes import tile, player

def test_tile_check_valid():
    tile1 = tile(3,3)
    tile1.update_letter('h')
    tile1.update_height()
    tile1.check_valid()
    
    assert tile1.get_valid() == True
    
    for i in range(5):
        tile1.update_height()
    tile1.check_valid()
    
    assert tile1.get_valid() == False
    
def test_player_update_hand():
    
    #Test replacing hand to full - removing all letters from bag
    p1 = player("p1", "ower", 0, 1)
    letters = ['a', 'b', 'c']
    
    p1.update_hand(p1.get_hand(), letters)
    assert len(p1.get_hand()) == 7
    assert len(letters) == 0
    
    #Test replacing hand to full - some letters still in bag
    p2 = player("p2", "ower", 0, 2)
    letters = ['a', 'b', 'c', 'd', 'e']    
    
    p2.update_hand(p2.get_hand(), letters)
    assert len(p2.get_hand()) == 7
    assert len(letters) == 2
    
    #Test replacing hand with bag empty
    p3 = player("p3", "ower", 0, 3)
    letters = []    
    
    p3.update_hand(p3.get_hand(), letters)
    assert len(p3.get_hand()) == 4
    assert len(letters) == 0
    
    #Test replacing hand with bag running out partway through
    p4 = player("p4", "ower", 0, 4)
    letters = ['a', 'b']    

    p4.update_hand(p4.get_hand(), letters)
    assert len(p4.get_hand()) == 6
    assert len(letters) == 0    
    
    #Test replacing hand with qu tile
    p5 = player("p5", "abc(qu)", 0, 5)
    
    letters = ['a', 'b', 'c', 'd', 'e']
    
    p5.update_hand(p5.get_hand(), letters)
    assert len(p5.get_hand()) == 10
    assert len(letters) == 2