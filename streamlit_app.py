#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to run, but this hasn't been working in python - have had to switch to bash
#streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
#import functions as fxn
import gspread

st.title('Stillwater Tennis Association Summer Singles Ladder')

st.subheader('Current Player Standings')

#Access google sheet with player data
gc = gspread.service_account("/Users/jwiggi/.config/gspread/credentials.json")

#stopped working when i tried to cache the data
#@st.cache_data
#the google sheet with player data
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WUElZS0I_1EVgoew2AoRH9jzgSf5s7CI8-DQCyES3X4/edit#gid=0").sheet1

data = sh.get_all_records()

df = pd.DataFrame(data)

#remove spaces from column names
df.columns = df.columns.str.replace(' ', '')
#extract the first column of df (player names)
players = df.iloc[:, 0]

#display the player names
st.dataframe(players)

st.subheader('I would like to challenge: ')
player = st.selectbox('Select a player:', players)


#get the player's email
def get_email(player):
    return df.loc[df['Name'] == player, 'email']

#display the player's email
st.write('Cool! You would like to challenge ' + player + '. Email them at: ')
st.write(get_email(player))

#Section for players to enter match results
st.subheader('Enter Match Results')
winner = st.selectbox('Select the winner:', players)
loser = st.selectbox('Select the loser:', players)

st.write('Great! ' + winner + ' won the match against ' + loser + '.')

#update the players dataframe with the match results
def update_results(winner, loser):
    #get the current rankings of the players
    winner = winner
    loser = loser
    #Get the indices of the players (current rankings)
    winner_index = players.index.get_loc(players[players['Name'] == winner].index[0])
    loser_index = players.index.get_loc(players[players['Name'] == loser].index[0])
    
    #check if the loser is ranked higher than the winner
    if loser_index > winner_index:
        #if the loser is ranked higher than the winner, put the loser in the winner's spot and move the winner down one spot
        #store the row data of the winner
        winner_row = players.iloc[winner_index].copy()
        
        #shift the rows between loser and winner down by on position
        players.iloc[winner_index:loser_index] = players.iloc[winner_index+1:loser_index+1].values
        
        #put the winner in the loser's spot
        players.iloc[loser_index] = winner_row
        
        print('The winner has been moved up in the rankings.')
    else:
        #if the winner is ranked higher than the loser, do nothing
        print('The winner is ranked higher than the loser. No changes made.')
        
st.write(update_results(winner, loser))