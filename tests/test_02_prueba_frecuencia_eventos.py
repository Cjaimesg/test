# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:27:51 2022

@author: cajgo
"""


import pyodbc 
import pandas as pd
import sqlalchemy
import copy as copy

from datetime import datetime, timedelta

def find_seq_events(futuros_eventos, n_events = 5, duration_event = 2.5):
    
    source_eventId = futuros_eventos['eventId'].iloc[0]
    list_eventId = [source_eventId]
    for _ in range(n_events):
        eventId = list_eventId[-1]
        
        eventos_id = futuros_eventos[futuros_eventos['eventId'] == eventId][['eventId', 'start', 
                       'mainBetOffer_odds_0', 'mainBetOffer_odds_1', 'mainBetOffer_odds_2']]
        start_event = eventos_id['start'].iloc[0].to_pydatetime()
        
        end_event = start_event + timedelta(hours = duration_event)
        
        futuros_eventos = futuros_eventos[futuros_eventos['start'] >= end_event]
        try:
            next_eventId = futuros_eventos['eventId'].iloc[0]
        except IndexError:
            break
        list_eventId.append(next_eventId)
    
    return list_eventId
 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-LQRV86K;'
                      'Database=Odd_Sports;',
                      autocommit = True)
cursor = conn.cursor()

engine = sqlalchemy.create_engine(
                       "mssql+pyodbc://DESKTOP-LQRV86K/Odd_Sports?driver=SQL Server",
                       echo=False)

futuros_eventos = pd.read_sql("""
        select * from Odd_Sports.dbo.future_enfrentamientos

        where 
        mainBetOffer_odds_0 > 0 and
        mainBetOffer_odds_1 > 0 and 
        mainBetOffer_odds_2 > 0 and 
        sport = 'FOOTBALL'
        
        and start like 'Oct%'
        """,
                    engine, 
                    parse_dates=["start"])


dic_seq_estimadas = {}

tot_apostadores = 50
tot_events = 100

futuros_eventos = futuros_eventos.sort_values(by='start')
futuros_eventos = futuros_eventos.reset_index(drop = True)

futuros_events_selected = copy.copy(futuros_eventos)

for i in range(tot_apostadores):
    list_eventId = find_seq_events(futuros_eventos, n_events = tot_events)
    futuros_eventos = futuros_eventos[~futuros_eventos['eventId'].isin(list_eventId)]
    dic_seq_estimadas[i] = list_eventId
    
    
all_futuros_events_selected_i = pd.DataFrame()

for i_apostador in dic_seq_estimadas.keys():
    futuros_events_selected_i = futuros_events_selected[futuros_events_selected['eventId'].isin(dic_seq_estimadas[i_apostador])]
    
    futuros_events_selected_i = futuros_events_selected_i[['eventId', 'start', 'mainBetOffer_odds_0', 'mainBetOffer_odds_1', 'mainBetOffer_odds_2']]
    
    futuros_events_selected_i[['mainBetOffer_odds_0', 'mainBetOffer_odds_1', 'mainBetOffer_odds_2']] = futuros_events_selected_i[['mainBetOffer_odds_0', 'mainBetOffer_odds_1', 'mainBetOffer_odds_2']]/1000
    
    #futuros_events_selected_i = futuros_events_selected_i.set_index('eventId')
    
    futuros_events_selected_i['apostador'] = i_apostador
    
    all_futuros_events_selected_i = all_futuros_events_selected_i.append(futuros_events_selected_i)
        
    
    
futuros_events_selected = futuros_events_selected.merge(all_futuros_events_selected_i[['eventId', 'apostador']], on=['eventId'], how='left')
    
    
    
total_eventos_por_apostador = futuros_events_selected.groupby('apostador').count()['eventId']
tasa_de_eventos_apostados = total_eventos_por_apostador.sum()/futuros_events_selected.count()['eventId']











print('''1234\r987''')








