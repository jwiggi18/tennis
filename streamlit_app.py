#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to run, but this hasn't been working in python - have had to switch to bash
#streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import functions as fxn

st.title('Stillwater Tennis Association Summer Singles Ladder')

st.subheader('Current Player Standings')
st.dataframe(fxn.players)

st.subheader('I would like to challenge: ')
player = st.selectbox('Select a player:', fxn.players)

st.subheader('Cool! You would like to challenge ' + player + '. Email them at: ')
st.write(fxn.get_email(player))