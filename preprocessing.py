import pandas as pd
import numpy as np
import streamlit as st

filename = 'fifa_data.csv'
df = pd.read_csv(filename)

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
cat_cols = ['Preferred Foot', 'Work Rate', 'Position']

numerical_cols = numerical_cols[2:]

# passing score
passing_cols = ['Crossing', 'ShortPassing', 'LongPassing', 'Curve', 'FKAccuracy']
df['passing_score'] = df[passing_cols].mean(axis=1)
#ball control score
ball_control_cols = ['BallControl', 'Dribbling', 'Skill Moves', 'Acceleration', 'Balance']
df['ball_control_score'] = df[ball_control_cols].mean(axis=1)
#stamina score
stamina_cols = ['Stamina', 'Strength', 'Aggression', 'Jumping', 'SprintSpeed', 'Jumping', 'LongShots']
df['stamina_score'] = df[stamina_cols].mean(axis=1)
#gk score
gk_cols = ['GKHandling', 'GKDiving', 'GKKicking', 'GKPositioning', 'GKReflexes']
df['gk_score'] = df[gk_cols].mean(axis=1)
#tackling score
tackling_cols = ['StandingTackle', 'SlidingTackle', 'Interceptions', 'Marking']
df['tackling_score'] = df[tackling_cols].mean(axis=1)

added_features = ['passing_score', 'ball_control_score', 'stamina_score', 'gk_score', 'tackling_score']

input_num_features = numerical_cols.tolist() + added_features

work_rate_mapping = {
    'Low/ Low': 1,
    'Low/ Medium': 2,
    'Low/ High': 3,
    'Medium/ Low': 4,
    'Medium/ Medium': 5,
    'Medium/ High': 6,
    'High/ Low': 7,
    'High/ Medium': 8,
    'High/ High': 9
}

df['Work Rate'] = df['Work Rate'].map(work_rate_mapping)

positions = df['Position'].unique().tolist()

postion_map = {}
for (i,pos) in enumerate(positions):
    postion_map[pos] = i+1
df['Position'] = df['Position'].map(postion_map)

input_features = input_num_features + df[['Work Rate', 'Position']].columns.tolist()

def preprocess_input():
    player_names = df['Name'].tolist()
    selected_player = st.selectbox('Select a Player', player_names)
    selected_index = player_names.index(selected_player)
    player_data = df.loc[selected_index, input_features]
    return player_data.values.reshape(1, -1)
    