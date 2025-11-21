import pandas as pd
import numpy as np
import plotly.express as px
import math
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

filename = 'fifa_data.csv'
df = pd.read_csv(filename)

# age distribution
def age_distribution():
    fig = px.histogram(df, x='Age', nbins=50, title='Age Distribution of Players')
    st.image('age_distribution.png', use_container_width=True)

# features distribution
def features_distribution():
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns

    # Exclude first 2 columns if needed
    features = numerical_cols[2:]

    n_cols = 5
    n_rows = math.ceil(len(features) / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5 * n_rows))
    axes = axes.flatten()

    for i, col in enumerate(features):
        sns.histplot(df[col], bins=30, kde=True, color='lightgreen', ax=axes[i])
        axes[i].set_title(f"Distribution of {col}")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Count")

    for j in range(len(features), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)
    return None


# correlation heatmap
def correlation_heatmap():
    corr = df.select_dtypes(include=[np.number]).corr()
    fig = px.imshow(corr, title='Correlation Heatmap of Numerical Features')
    return fig


# added feature distribution
def added_feature_distribution():
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
    fig = px.histogram(featured_df.melt(), x='value', facet_col='variable', 
                       title='Distribution of Added Features', nbins=30)
    return fig


# categorical feature distribution
def categorical_feature_distribution():
    categorical_features = df.select_dtypes(include=['object'])
    fig = px.histogram(categorical_features.melt(), x='value', facet_col='variable', 
                       title='Distribution of Categorical Features', nbins=30)
    return fig



def get_full_analysis_fig(analysis_type):
    if analysis_type == 'Age Distribution':
        return age_distribution()
    elif analysis_type == 'Features Distribution':
        return features_distribution()
    elif analysis_type == 'Correlation Heatmap':
        st.image('correlation_heatmap.png', use_container_width=True)
    elif analysis_type == 'Added Feature Distribution':
        st.image('added_features.png', use_container_width=True)
    elif analysis_type == 'Categorical Feature Distribution':
        st.image('cat_features.png', use_container_width=True)
    else:
        return None