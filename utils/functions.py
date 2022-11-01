# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:05:58 2022

@author: cajgo
"""


import numpy as np
import pandas as pd

def select_odd(lossing_strick, odds, min_bet_allowed, money_to_recover):
#    if lossing_strick == 0:
#        selected_odd = np.amin(odds, axis=0)
#        selected_winner = odds.index(selected_odd)
    
    selected_odd = np.amin(odds, axis=0)
    selected_winner = odds.index(selected_odd)
        
#    else :
#        selected_odd = np.amin(odds, axis=0)
#        selected_winner = odds.index(selected_odd)
#        money_bet = -money_to_recover/selected_odd
#        
#        if money_bet < min_bet_allowed:
#            
#            selected_odd = sorted(set(odds))[1]
#            selected_winner = odds.index(selected_odd)
#            money_bet = -money_to_recover/selected_odd
            
        
    
    return selected_odd, selected_winner