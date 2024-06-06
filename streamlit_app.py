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


#Access google sheet with player data
gc = gspread.service_account("/Users/jwiggi/.config/gspread/credentials.json")

#stopped working when i tried to cache the data
#@st.cache_data
#the google sheet with player data
def load_data():
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WUElZS0I_1EVgoew2AoRH9jzgSf5s7CI8-DQCyES3X4/edit#gid=0").sheet1
    data = sh.get_all_records()
    return pd.DataFrame(data)

df = load_data()

#remove spaces from column names
df.columns = df.columns.str.replace(' ', '')

#extract the first column of df (player names)
players = df.iloc[:, 0]
#convert the series 'players' to a dataframe
players = pd.DataFrame(players, columns=['Name'])
#make players index start at 1
players.index = df.index + 1

# Initialize session state to store player data
if 'players' not in st.session_state:
    st.session_state.players = players


# Initialize session state to track previous selection
if 'previous_player' not in st.session_state:
    st.session_state.previous_player = None
 
col1, col2 = st.columns(2)
with col1:
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
        st.session_state.players['Name'],
        index=None, 
        placeholder='Select the winner'
    )
    loser = st.selectbox(
        'Select the loser:', 
        st.session_state.players['Name'],
        index=None, 
        placeholder='Select the loser'
    )


    #update the players dataframe with the match results

    def update_results(winner, loser, players):
        #Get the indices of the players (current rankings)
        winner_index = players[players['Name'] == winner].index[0]
        loser_index = players[players['Name'] == loser].index[0]
        #check if the winner index is larger (lower in the rankings) than the loser index
        if loser_index < winner_index:
            #make a list the length of the players DataFrame
            new_order = list(range(len(players)))
            #remove the winner from the list
            new_order.pop(winner_index)
            #insert the winner at the loser's index
            new_order.insert(loser_index, winner_index)
            #reindex the DataFrame
            players = players.reindex(new_order).reset_index(drop=True)
            players.index = df.index + 1
            st.write('The winner has been moved up in the rankings.')
            print(players)
        else:
            #if the winner is ranked higher than the loser, do nothing
            st.write('The winner is ranked higher than the loser. No changes made.')
            
        return players

    #Button to trigger the update_results function
    if st.button('Submit Match Results'):
        st.session_state.players = update_results(winner, loser, st.session_state.players.copy())
       
    #call the function and display the updated player rankings
    if winner and loser:
        st.write('Great! ' + winner + ' won the match against ' + loser + '.')

with col2:
    st.subheader('Current Player Standings')
    #Display the updated player rankings
    st.dataframe(st.session_state.players)