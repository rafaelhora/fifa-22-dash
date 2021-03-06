import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
#import chart_studio.plotly as py
import cufflinks as cf
import plotly.express as px

st.set_page_config(layout="wide")

container_intro = st.container()
with container_intro:
    st.title('FIFA 22 Companion Dashboard')
    st.subheader('This is an companion app containing all players from the FIFA 22 roster. This can help you find players for your career mode, and choose with which team to play.')


## Page Elements
def options_sidebar():
    st.sidebar.markdown('# Options')


# sidebar
st.sidebar.title('Options sidebar')

## Helpers

#import and clean dataset
@st.cache
def get_data():
    #get dataset and separate information not used for analysis
    df = pd.read_csv('FIFA22_official_data.csv')
    df_extra_info = df[['ID','Photo', 'Flag', 'Club Logo', 'Real Face']]

    #data cleaning  
    df.drop(columns=['Photo', 'Flag', 'Club Logo', 'Real Face'], inplace=True)
    df['Wage'] = df['Wage'].replace({'€': '', ',': '', 'K':'000', '\.':''}, regex=True).astype(float)
    df['Release Clause'] = df['Release Clause'].replace({'€': '', ',': '', 'K':'000','M':'000000', '\.':''}, regex=True).astype(float)
    df['Value'] = df['Value'].replace({'€': '', ',': '', 'K':'000', 'M':'000000', '\.':''}, regex=True).astype(float)
    df['Weight'] = df['Weight'].replace({'kg':''}, regex=True).astype(float)
    df['Height'] = df['Height'].replace({'cm':''}, regex=True).astype(float)
    df['Wage'] = df['Wage']/1000
    df['Release Clause'] = df['Release Clause']/1000000
    df['Value'] = df['Value']/1000000
    
    return df, df_extra_info


df, df_extra = get_data()

#download raw dataset
st.sidebar.download_button("Download Raw Dataset",data='FIFA22_official_data.csv' )


# total value of club roster
def all_clubs_value():
    values = df.groupby('Club', as_index=False).sum()[['Club','Value']].reset_index()
    values = values.sort_values('Value', ascending = False).iloc[:10]
    values.set_index('Club', inplace=True)
    return values

# total club monthly wage
def all_clubs_wage():
    wages = df.groupby('Club', as_index=False).sum()[['Club','Wage']].reset_index()
    wages = wages.sort_values('Wage', ascending = False).iloc[:10]
    wages.set_index('Club', inplace=True)
    return wages

#show most promising players

# Apps

## Show most promising players

def most_promising(wage_range, value_range, age_range, current_rating_range, potential_range, future_growth_range, player_position, top_n):
    promising_players = df[['ID', 'Name', 'Age','Club','Best Position','Best Overall Rating', 'Potential','Value', 'Wage']]
    promising_players['future_growth'] = promising_players['Potential'] - promising_players['Best Overall Rating']
    promising_players = promising_players.sort_values(['future_growth', 'Potential'], ascending = False)
    promising_players = promising_players[promising_players['Wage'].between(wage_range[0], wage_range[1]) 
                                          & promising_players['Value'].between(value_range[0], value_range[1])  
                                          & promising_players['Age'].between(age_range[0], age_range[1]) 
                                          & promising_players['Best Overall Rating'].between(current_rating_range[0], current_rating_range[1]) 
                                          & promising_players['Potential'].between(potential_range[0], potential_range[1])
                                          & promising_players['future_growth'].between(future_growth_range[0], future_growth_range[1])
                                          & promising_players['Best Position'].isin(player_position)]
    promising_players = promising_players.iloc[:int(top_n)]
    return promising_players

## Most promising players
'''
## Most promising Players
'''
#columns
col1, col2 = st.columns(2)
with col1:
    wage_range = st.slider("Wage Range (in €1K)", min(df.Wage), max(df.Wage),(min(df.Wage), max(df.Wage)), step = 0.5, format = '%f')
    value_range = st.slider("Value Range (in €1MM)", min(df.Value), max(df.Value),(min(df.Value), max(df.Value)), step = 0.5, format = '%f')
    age_range = st.slider("Age Range", min(df.Age), max(df.Age),(min(df.Age), max(df.Age)))
    player_position = st.multiselect("Player Best Postition", options = df['Best Position'].unique(), default = df['Best Position'].unique())
with col2:
    current_rating_range = st.slider("Current rating", min(df['Best Overall Rating']), max(df['Best Overall Rating']), (min(df['Best Overall Rating']), max(df['Best Overall Rating'])), format = '%d')
    potential_range = st.slider("Potential", min(df['Potential']), max(df['Potential']), (min(df['Potential']), max(df['Potential'])))
    future_growth_range = st.slider("Growth", min(df['Potential'] - df['Best Overall Rating']), max(df['Potential'] - df['Best Overall Rating']), (min(df['Potential'] - df['Best Overall Rating']), max(df['Potential'] - df['Best Overall Rating'])), format = '%d')
    top_n = st.number_input("Display limit", min_value = 1, max_value = len(df.index), value = 20)


#attributes = ['Age', 'Wage', 'Value', 'Current Rating', 'Potential', 'Best Position']
#order_promising_players = st.multiselect("Order By", attributes)

df_most_promising = most_promising(wage_range, value_range, age_range, current_rating_range, potential_range, future_growth_range, player_position, top_n)

st.dataframe(df_most_promising.style.highlight_max(axis = 0, color = 'green').hide_index())
st.download_button('Download data', df_most_promising.to_csv())


## Show club details

st.empty()

#returns the overview of a club's information
def view_club(df, club):
    
    df_club = df[df['Club'] == club]
    
    club_value = str(float('%.2f' % df_club['Value'].sum()))
    club_value = '€ ' + club_value + 'MM'
    
    club_wage = str(float('%.2f' % df_club['Wage'].sum()))
    club_wage = '€ ' + club_wage + 'K'
    
    club_avg_age = float('%.2f' % df_club['Age'].mean())
    club_avg_rating = float('%.2f' % df_club['Best Overall Rating'].mean())
    
    club_avg_value = str(float('%.2f' % df_club['Value'].mean()))
    club_avg_value = '€ ' + club_avg_value + 'MM'
    
    club_avg_wage = str(float('%.2f' % df_club['Wage'].mean()))
    club_avg_wage = '€ ' + club_avg_wage + 'K'
    
    return club_value, club_wage, club_avg_age, club_avg_rating, club_avg_wage, club_avg_value, df_club

'''
## League Overview
'''

club = st.selectbox('Select a team', options = df.Club.unique())

club_value, club_wage, club_avg_age, club_avg_rating, club_avg_wage, club_avg_value, df_club = view_club(df, club)

col3, col4, col5 = st.columns(3)

st.write('###', club)
with col3:
    st.metric('Total Roster Value', club_value)
    st.metric('Total Wage Cost', club_wage)
with col4:
    st.metric('Average Player Wage', club_avg_wage)
    st.metric('Average Player Value', club_avg_value)
with col5:
    st.metric('Average Player Wage', club_avg_age)
    st.metric('Average Player Rating', club_avg_rating)

st.dataframe(df_club)