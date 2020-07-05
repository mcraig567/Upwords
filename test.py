# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:35:54 2020

@author: craig
"""

from colorama import Fore
from colorama import Style
from colorama import Back

# grid = [[0]*8 for n in range (10)]

# for row in grid:
#     print(row)
    
# print()    
    
# grid[5][5] = 4

# for row in grid:
#     print(row)
    
# print()    
    
# grid[5][5] = 'r'

# for row in grid:
#     print(row)
    

# hand_copy = 'abcdaaef'
# hand_copy = hand_copy.replace('a', '', 2)

# # print(hand_copy)

# scores = [50, 20, 5]
# names = ["Matt", "Benjamin", "Ana"]

# print("%-6s %-10s %s" %("Rank", "Name", "Score"))
# for i in range(len(scores)):
#     print("%-6s %-10s %i" %(i + 1, names[i], scores[i]))
    
word = "queen"
red = '\033[93m'

print(f"This is {Fore.GREEN}colour{Style.RESET_ALL}!")    
print(f"This is a word: {Back.RED}%-10s{Style.RESET_ALL}!" %(word))

    