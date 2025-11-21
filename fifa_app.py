import streamlit as st
import pandas as pd
import numpy as np
from radar import radar_chart, radar_chart_comparison
from data_analysis import *
from preprocessing import *

import joblib
import gzip

with gzip.open("fifa_value_model_compressed.pkl.gz", "rb") as f:
    model = joblib.load(f)


filename = 'fifa_data.csv'
df = pd.read_csv(filename)
st.set_page_config(layout="wide")

st.title('FIFA Player Data')

buttons = st.radio(
    "Choose an option:",
    ('View Player Radar Chart','Compare Two Players', 'Full Analysis', 'Predict Player Value', 'Player Dashboard')
)
if buttons == 'View Player Radar Chart':
    player_names = df['Name'].tolist()
    selected_player = st.selectbox('Select a Player', player_names)
    selected_index = player_names.index(selected_player)
    fig = radar_chart(selected_index)
    st.plotly_chart(fig)

elif buttons == 'Compare Two Players':
    player_names = df['Name'].tolist()
    selected_player1 = st.selectbox('Select First Player', player_names, key='player1')
    selected_player2 = st.selectbox('Select Second Player', player_names, key='player2')
    index1 = player_names.index(selected_player1)
    index2 = player_names.index(selected_player2)
    fig = radar_chart_comparison(index1, index2)
    st.plotly_chart(fig)

elif buttons == 'Full Analysis':
    buttons = st.selectbox(
        "Choose Analysis Type:",
        ('Age Distribution', 'Features Distribution',
         'Correlation Heatmap', 'Added Feature Distribution', 'Categorical Feature Distribution'
        ))
    fig = get_full_analysis_fig(buttons)
    if fig:
        st.plotly_chart(fig)
elif buttons == 'Predict Player Value':
    player_data = preprocess_input()
    input_data = np.array(player_data).reshape(1, -1)
    predicted_value = model.predict(input_data)[0]
    st.write(f"Predicted Market Value: €{predicted_value:,.2f} M")

elif buttons == 'Player Dashboard':

    st.subheader("Player Dashboard")

    player_names = df['Name'].tolist()
    selected_player = st.selectbox('Select a Player', player_names)

    player_row = df[df['Name'] == selected_player].iloc[0]

    stat_columns = ['Overall', 'Potential',
       'International Reputation', 'Weak Foot', 'Skill Moves',
       'Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys',
       'Dribbling', 'Curve', 'FKAccuracy', 'LongPassing', 'BallControl',
       'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
       'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots',
       'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
       'Composure', 'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving',
       'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']

    st.markdown(
        """
        <style>
        .glow-container {
            border: 2px solid #00FFFF;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 0 20px #00FFFF;
            background-color: #0d0f15;
        }
        .stat-label {
            color: #E0E0E0;
            font-size: 14px;
            font-weight: 500;
        }
        .stat-bar-container {
            width: 100%;
            background-color: #1e1e1e;
            height: 8px;
            border-radius: 5px;
            margin: 3px 0 12px 0;
        }
        .stat-bar-fill {
            height: 8px;
            background-color: #32CD32;
            border-radius: 5px;
        }
        .player-title {
            text-align: center;
            font-size: 38px;
            font-weight: 700;
            color: #00FFFF;
            margin-bottom: 25px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<div class='glow-container'>", unsafe_allow_html=True)

    st.markdown(f"<div class='player-title'>{selected_player}</div>", unsafe_allow_html=True)

    cols = st.columns(3)

    special_stats = ['International Reputation', 'Weak Foot', 'Skill Moves']

    for i, stat in enumerate(stat_columns):
        col = cols[i % 3]
    
        raw = player_row.get(stat, 0)
        try:
            value = float(raw)
        except Exception:
            value = 0.0
    
        if stat in special_stats:
            scaled_value = min(max((value / 5.0) * 100.0, 0.0), 100.0)
            if float(value).is_integer():
                display_value = f"{int(value)}/5"
            else:
                display_value = f"{value:.1f}/5"
        else:
            scaled_value = min(max(value, 0.0), 100.0)
            if float(value).is_integer():
                display_value = f"{int(value)}"
            else:
                display_value = f"{value:.1f}"
    
        bar_color = "#FF4C4C" if scaled_value < 50 else "#32CD32"   
    
        col.markdown(
            f"""
            <div>
                <div class="stat-label">{stat}: <span style="color:#CFCFCF;">{display_value}</span></div>
                <div class="stat-bar-container">
                    <div class="stat-bar-fill" style="width:{scaled_value}%; background:{bar_color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<hr style='border:1px solid #00FFFF;'>", unsafe_allow_html=True)
    st.subheader("Radar Chart")
    index = player_names.index(selected_player)
    fig = radar_chart(index)
    st.plotly_chart(fig)
    st.markdown("</div>", unsafe_allow_html=True)