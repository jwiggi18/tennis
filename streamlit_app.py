#!/usr/bin/env python
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import functions as fxn

st.title('Stillwater Tennis Association Summer Singles Ladder')

# Sign up sheet URL
url =''
#convert the url to csv
csv_url = fxn.convert_google_sheet_url(url)
#read in the csv
start_ladder = pd.read_csv(csv_url)