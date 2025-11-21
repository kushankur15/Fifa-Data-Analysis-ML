import pandas as pd
import numpy as np
import plotly.express as px

filename = 'fifa_data.csv'
df = pd.read_csv(filename)

numerical_features = df.select_dtypes(include=[np.number])
numerical_features.columns.tolist()
numerical_features = numerical_features.drop(columns=['Unnamed: 0','ID', 'Age', 'Overall', 'Potential', 'Special'])

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

featured_df = df[['passing_score', 'ball_control_score', 'stamina_score', 'gk_score', 'tackling_score']]



def radar_chart(index):
    player = featured_df.iloc[index]
    name = df['Name'].iloc[index]
    labels = player.index.tolist()
    stats = player.values.tolist()

    fig = px.line_polar(
        r=stats + [stats[0]],
        theta=labels + [labels[0]],
        line_close=True,
        title=f'Player Radar Chart: {name}'
    )
    fig.update_traces(fill='toself', opacity=0.6)
    return fig

def radar_chart_comparison(index1, index2):
    custom_colors = ['#1f77b4', '#ff7f0e']
    players = featured_df.iloc[[index1, index2]]
    names = df['Name'].iloc[[index1, index2]].tolist()
    players["Player"] = names

    labels = players.columns.tolist()
    stats1 = players.iloc[0].values.tolist()
    stats2 = players.iloc[1].values.tolist()

    players_melted = players.reset_index().melt(id_vars='Player', var_name='skill', value_name='value')

    fig = px.line_polar(
        players_melted,
        r = "value",
        theta = "skill",
        color = "Player",
        line_close=True,
        title=f'Player Radar Chart Comparison: {names[0]} vs {names[1]}',
        color_discrete_sequence=custom_colors
    )
    fig.update_traces(fill='toself', opacity=0.4)
    return fig
    