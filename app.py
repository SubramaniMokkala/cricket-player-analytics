import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="IPL Player Analytics",
    page_icon="🏏",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        padding: 30px;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏏 IPL Player Performance Analytics</div>', 
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load data and model
@st.cache_resource
def load_resources():
    player_stats = pd.read_csv('data/player_statistics.csv')
    model = joblib.load('models/player_performance_model.pkl')
    scaler = joblib.load('models/player_scaler.pkl')
    return player_stats, model, scaler

player_stats, model, scaler = load_resources()

# Sidebar
st.sidebar.title("🎛️ Player Selector")
st.sidebar.markdown("---")

# Filter by role
role_filter = st.sidebar.multiselect(
    "Select Role:",
    options=['Batsman', 'Bowler', 'All-rounder'],
    default=['Batsman', 'All-rounder']
)

filtered_players = player_stats[player_stats['role'].isin(role_filter)]

# Select player
player_name = st.sidebar.selectbox(
    "Select Player:",
    options=sorted(filtered_players['player'].unique())
)

# Get player data
player_data = player_stats[player_stats['player'] == player_name].iloc[0]

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"## 👤 {player_name}")
    st.markdown(f"**Role:** {player_data['role']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Batting Stats
    if player_data['role'] in ['Batsman', 'All-rounder']:
        st.markdown("### 🏏 Batting Statistics")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Runs", f"{int(player_data['total_runs'])}")
        col_b.metric("Average", f"{player_data['batting_average']:.2f}")
        col_c.metric("Strike Rate", f"{player_data['strike_rate']:.2f}")
        
        col_d, col_e, col_f = st.columns(3)
        col_d.metric("Matches", f"{int(player_data['matches_played'])}")
        col_e.metric("Fours", f"{int(player_data['fours'])}")
        col_f.metric("Sixes", f"{int(player_data['sixes'])}")

with col2:
    # ML Prediction
    if player_data['role'] in ['Batsman', 'All-rounder'] and player_data['total_runs'] > 200:
        st.markdown("### 🎯 Performance Prediction")
        
        features = [[
            player_data['strike_rate'],
            player_data['fours'],
            player_data['sixes'],
            player_data['balls_faced'],
            player_data['matches_played'],
            player_data['times_out']
        ]]
        
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        category = "High Performer" if prediction == 1 else "Regular Performer"
        color = "#2ecc71" if prediction == 1 else "#f39c12"
        confidence = prediction_proba[prediction] * 100
        
        st.markdown(f"""
            <div style='background-color: {color}; padding: 30px; border-radius: 15px; 
                        text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h2 style='color: white; margin: 0;'>{category}</h2>
                <p style='color: white; font-size: 20px; margin-top: 10px;'>
                    Confidence: {confidence:.1f}%
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Probability gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction_proba[1] * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "High Performer Probability (%)", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

# Bowling Stats
if player_data['role'] in ['Bowler', 'All-rounder'] and player_data['wickets'] > 0:
    st.markdown("---")
    st.markdown("### 🎯 Bowling Statistics")
    
    col_g, col_h, col_i, col_j = st.columns(4)
    col_g.metric("Wickets", f"{int(player_data['wickets'])}")
    col_h.metric("Economy", f"{player_data['economy_rate']:.2f}")
    col_i.metric("Average", f"{player_data['bowling_average']:.2f}")
    col_j.metric("Matches", f"{int(player_data['matches_bowled'])}")

# Comparison with league average
st.markdown("---")
st.markdown("## 📊 Comparison with League Average")

if player_data['role'] in ['Batsman', 'All-rounder']:
    metrics_comparison = pd.DataFrame({
        'Metric': ['Batting Average', 'Strike Rate', 'Runs per Match'],
        'Player': [
            player_data['batting_average'],
            player_data['strike_rate'],
            player_data['total_runs'] / player_data['matches_played']
        ],
        'League Average': [
            filtered_players['batting_average'].mean(),
            filtered_players['strike_rate'].mean(),
            (filtered_players['total_runs'] / filtered_players['matches_played']).mean()
        ]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Player', x=metrics_comparison['Metric'], y=metrics_comparison['Player'],
                        marker_color='#3498db'))
    fig.add_trace(go.Bar(name='League Avg', x=metrics_comparison['Metric'], y=metrics_comparison['League Average'],
                        marker_color='#95a5a6'))
    
    fig.update_layout(
        title="Player vs League Average",
        xaxis_title="Metrics",
        yaxis_title="Value",
        height=400,
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p><strong>IPL Player Performance Analytics</strong></p>
        <p>ML Model: Random Forest (84.62% Accuracy) | Data: IPL 2008-2020</p>
        <p>Author: Subramani Mokkala | November 2025</p>
    </div>
""", unsafe_allow_html=True)