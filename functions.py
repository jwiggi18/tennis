
import pandas as pd
import gspread

gc = gspread.service_account("/Users/jwiggi/.config/gspread/credentials.json") #hangs here

#cache so don't have to reload the data every time
@st.cache_data
#the google sheet with player data
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WUElZS0I_1EVgoew2AoRH9jzgSf5s7CI8-DQCyES3X4/edit#gid=0").sheet1

data = sh.get_all_records()

df = pd.DataFrame(data)

df.head()

#extract the first column of df (player names)
players = df.iloc[:, 0]

players.head()

#function to get the players email based on input from the user
def get_email(player):
    return df.loc[df['Name'] == player, 'email']

df.loc[df['Name'] == 'Will Wiggins', 'email']


#does the fxn work?
print(get_email('Will Wiggins'))