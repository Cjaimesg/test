# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 08:27:00 2022

@author: cajgo
"""

import pandas as pd 
import numpy as np
import time

import recover_strategy.utils.functions as f





number_of_total_odds = 20000

#TODO registrar el comportamiento de los escneanrios, dinero total invertidfo 
#racha de perdida etc 

min_bet_allowed = 500
base_money_bet = 2000
tot_eventos = 1000

min_selected_bet = 1.1

money_win = pd.DataFrame()

money_win_dic = {}

for j in range(2):
    a = time.time()
    for i in range(tot_eventos):
        #print('--'*30)
        
        pr = np.random.dirichlet(np.ones(3),size=number_of_total_odds)
        
        odd = 1/(pr + np.random.dirichlet(np.ones(3),size=number_of_total_odds)/10)
    
        df_pr = pd.DataFrame(pr, columns = ['pr_home', 'pr_draw', 'pr_away'])
        df_odd = pd.DataFrame(odd, columns = ['odd_home', 'odd_draw', 'odd_away'])
        df_stra = pd.concat([df_pr, df_odd], axis = 1)
        
        
        df_stra = df_stra[df_stra['odd_home'] > min_selected_bet]
        df_stra = df_stra[df_stra['odd_draw'] > min_selected_bet]
        df_stra = df_stra[df_stra['odd_away'] > min_selected_bet]
        
        lossing_strick = 0
        
        money_bet = base_money_bet
        money_winned_by_seq = 0
        money_to_recover = 0
        
        tot_money_bet = 0
        min_bet = money_bet
        
        
        for row in df_stra.itertuples():    
            winner = np.random.choice(3, 1, p=[row.pr_home, row.pr_draw, row.pr_away])
            odds = [row.odd_home, row.odd_draw, row.odd_away]
            selected_odd, selected_winner = f.select_odd(lossing_strick, odds, min_bet_allowed, money_to_recover)
            
            if money_to_recover < 0:
                money_bet = -money_to_recover/(selected_odd-1)
                
            tot_money_bet += money_bet
            if min_bet > money_bet:
                min_bet = money_bet
            
                
            if winner[0] == selected_winner:
                money_winned_by_seq += money_bet * selected_odd
                
                money_win_dic[i] = {
                        'money_winned_by_seq' : money_winned_by_seq-money_bet,
                        'lossing_strick'      : lossing_strick,
                        'tot_money_bet'       : tot_money_bet,
                        'min_bet'             : min_bet,
                        'money_bet'           : money_bet,
                        'selected_odd'        : selected_odd
                        }
                break
            
            else :
                lossing_strick += 1
                money_winned_by_seq -= money_bet
                #print(lossing_strick, money_winned_by_seq, selected_odd)
            money_to_recover = money_winned_by_seq
    
    
    #money_win.columns = ['money_winned_by_seq', 'lossing_strick', 'tot_money_bet', 'min_bet', 'last_money_bet', 'last_selected_odd']
            
    money_win = pd.DataFrame.from_dict(money_win_dic, orient='index')
    
    b = time.time()
    
    
    print('--'*30)
    print(j)
    print((b-a)/60)
    
    print(money_win['money_winned_by_seq'].sum()/tot_eventos/base_money_bet)
    print(100 * money_win[money_win['tot_money_bet'] > 1e+6]['money_winned_by_seq'].count()/tot_eventos)
    






(money_win['lossing_strick'] + 1).sum()






