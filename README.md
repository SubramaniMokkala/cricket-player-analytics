# 🏏 IPL Player Performance Analytics

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![ML](https://img.shields.io/badge/ML-Random%20Forest-green.svg)

Machine learning-powered analytics platform for IPL cricket player performance prediction and analysis.

![Dashboard](outputs/visualizations/dashboard_preview.png)

## 🎯 Overview

This project analyzes IPL (Indian Premier League) player statistics from 2008-2020 and uses machine learning to predict player performance categories. With **84.62% accuracy**, the Random Forest model classifies players as "High Performers" or "Regular Performers" based on their career statistics.

### Key Features

- **Real IPL Data**: 1,095 matches, 260,920 ball-by-ball records, 299 players
- **ML Model**: Random Forest classifier with 84.62% accuracy
- **Interactive Dashboard**: Streamlit web application for player lookup
- **Comprehensive Analysis**: Batting, bowling, and performance metrics
- **Professional Visualizations**: Plotly charts and statistical analysis

## 📊 Dataset

**Source**: Kaggle IPL Complete Dataset (2008-2020)

- **Matches**: 1,095 IPL matches
- **Deliveries**: 260,920 ball-by-ball records
- **Players**: 299 significant players (20+ matches)
- **Features**: Batting average, strike rate, wickets, economy rate, and more

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
pip
```

### Setup
```bash
git clone https://github.com/SubramaniMokkala/cricket-player-analytics.git
cd cricket-player-analytics
pip install -r requirements.txt
```

### Run Dashboard
```bash
streamlit run app.py
```

## 📁 Project Structure
```
cricket-player-analytics/
├── app.py                              # Streamlit dashboard
├── data/
│   ├── matches.csv                     # IPL match data
│   ├── deliveries.csv                  # Ball-by-ball data
│   └── player_statistics.csv           # Processed player stats
├── models/
│   ├── player_performance_model.pkl    # Trained Random Forest
│   └── player_scaler.pkl               # Feature scaler
├── notebooks/
│   ├── 01_player_performance_analysis.ipynb
│   └── 02_ml_model_training.ipynb
├── outputs/
│   └── visualizations/                 # Analysis charts
├── src/
│   ├── load_data.py
│   └── process_player_stats.py
└── README.md
```

## 🎓 Methodology

### 1. Data Processing
- Aggregated ball-by-ball deliveries into player statistics
- Calculated batting (average, strike rate) and bowling metrics (economy, wickets)
- Classified players into roles: Batsman, Bowler, All-rounder

### 2. Feature Engineering
- Selected 6 key features: strike_rate, fours, sixes, balls_faced, matches_played, times_out
- Created target variable: High Performer (batting avg > 25)
- Applied StandardScaler for feature normalization

### 3. Model Training
- Trained Random Forest (100 trees, max_depth=8)
- Trained Logistic Regression for comparison
- 80-20 train-test split with stratification

### 4. Deployment
- Built interactive Streamlit dashboard
- Real-time player lookup and prediction

## 📈 Results

### Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **Random Forest** | **84.62%** | 0.85 | 0.85 | 0.85 |
| Logistic Regression | 82.05% | - | - | - |

### Feature Importance

1. **balls_faced** - 24.5%
2. **fours** - 21.4%
3. **sixes** - 17.9%
4. **times_out** - 15.1%
5. **strike_rate** - 12.0%

### Key Insights

- **Top Run Scorer**: Virat Kohli (8,014 runs)
- **Top Wicket Taker**: Yuzvendra Chahal (213 wickets)
- **Average Strike Rate**: 129.8
- **Best Economy Rate**: 6.76 (Sunil Narine)

## 🛠️ Technologies Used

- **Python 3.13**: Core programming
- **Pandas & NumPy**: Data manipulation
- **Scikit-learn**: Machine learning
- **Streamlit**: Web dashboard
- **Plotly**: Interactive visualizations
- **Matplotlib & Seaborn**: Statistical plots

## 🎯 Use Cases

- **Player scouting**: Identify high-potential players
- **Team selection**: Data-driven team composition
- **Performance analysis**: Track player consistency
- **Fantasy cricket**: Statistical insights for team building

## 👤 Author

**Subramani Mokkala**
- 🎓 B.Tech in Computer Science - Data Science
- 📧 subramanimokkala@gmail.com
- 🔗 [SubramaniMokkala](https://www.linkedin.com/in/subramani-mokkala-727683245/)


## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Kaggle for IPL dataset
- IPL and BCCI for cricket data
- Streamlit for web framework

## 🚀 Future Enhancements

- Add more ML models (XGBoost, Neural Networks)
- Include recent IPL seasons (2021-2024)
- Player comparison feature
- Match outcome prediction
- Live data integration

---

**⭐ If you find this project useful, please consider giving it a star!**