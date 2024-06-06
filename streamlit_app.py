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
#convert the series 'players' to a dataframe
players = pd.DataFrame(players, columns=['Name'])

#display the player names
st.dataframe(players)

# Initialize session state to track previous selection
if 'previous_player' not in st.session_state:
    st.session_state.previous_player = None
    
st.subheader('Challenge a player')    
#player to challenge selection
player = st.selectbox(
   "Who would you like to challenge?",
   players['Name'],
   index=None,
   placeholder="Select a player...",
)

# Check if the selection has changed
if player != st.session_state.previous_player:
    # Get the player's email
    def get_email(player):
        return df.loc[df['Name'] == player, 'email'].values[0]

    #display the player's email
    st.write('Cool! You would like to challenge ' + player + '. Email them at: ')
    st.write(get_email(player))
    
    #update the previous player selection
    st.session_state.previous_player = player

#Section for players to enter match results
st.subheader('Enter Match Results')
winner = st.selectbox(
    'Select the winner:', 
    players['Name'],
    index=None, 
    placeholder='Select the winner'
)
loser = st.selectbox(
    'Select the loser:', 
    players['Name'],
    index=None, 
    placeholder='Select the loser'
)

if winner and loser:
    st.write('Great! ' + winner + ' won the match against ' + loser + '.')


#update the players dataframe with the match results
'''
def update_results(winner, loser, players):

    #Get the indices of the players (current rankings)
    winner_index = players[players['Name'] == winner].index[0]
    loser_index = players[players['Name'] == loser].index[0]

    #check if the winner index is larger (lower in the rankings) than the loser index
    if loser_index < winner_index:
        #reindex the DataFrame
        new_order = list(range(len(players)))
        #remove the winner from the list
        new_order.pop(winner_index)
        #insert the loser at the winner's index
        new_order.insert(loser_index, winner_index)
        #reindex the DataFrame
        players_updated = players.reindex(new_order).reset_index(drop=True)
            
        print('The winner has been moved up in the rankings.')
        return players_updated
    else:
        #if the winner is ranked higher than the loser, do nothing
        print('The winner is ranked higher than the loser. No changes made.')
    
        
 
        
#call the function and display the updated player rankings
#updated_players = update_results(winner, loser, players.copy())
st.write(update_results(winner, loser, players))
'''