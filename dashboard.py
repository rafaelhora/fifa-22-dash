import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

container_intro = st.container()
with container_intro:
    st.title('FIFA 22 Companion Dashboard')
    st.subheader('This is an companion app containing all players from the FIFA 22 roster. This can help you find players for your career mode, and choose with which team to play.')
    st.warning('Caution, showing the raw dataset can take minutes.')



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

    return df, df_extra_info

# total value of club roster
def club_value():
    values = df.groupby('Club', as_index=False).sum()[['Club','Value']].reset_index()
    values = values.sort_values('Value', ascending = False).iloc[:10]
    values.set_index('Club', inplace=True)
    return values

# total club monthly wage
def club_wage():
    wages = df.groupby('Club', as_index=False).sum()[['Club','Wage']].reset_index()
    wages = wages.sort_values('Wage', ascending = False).iloc[:10]
    wages.set_index('Club', inplace=True)
    return wages

def show_raw_data():
    if container_intro.checkbox('Show Raw Data') == True:
        st.dataframe(df)
    else:
        return

df, df_extra = get_data()
data = show_raw_data()

## Plots




## Page Elements
def options_sidebar(options):
    st.sidebar.markdown('# Options')


# sidebar
st.sidebar.title('Options sidebar')
st.sidebar.button('Click me')

#columns
col1, col2 = st.columns(2)


#Club information
with col1:
    st.bar_chart(club_value())

with col2:
    st.bar_chart(club_wage())
