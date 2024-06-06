# playing with examples to figure out what I am doing wrong

#to run, but this hasn't been working in python - have had to switch to bash
#streamlit run examples_app.py

import streamlit as st

option = st.selectbox(
   "How would you like to be contacted?",
   ("Email", "Home phone", "Mobile phone"),
   index=None,
   placeholder="Select contact method...",
)

st.write("You selected:", option)