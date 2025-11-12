import pandas as pd
import numpy as np

print("=" * 70)
print("PROCESSING PLAYER STATISTICS")
print("=" * 70)

# Load data
matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

print(f"\n✓ Loaded {len(matches)} matches and {len(deliveries)} deliveries")

# ===== BATTING STATISTICS =====
print("\nCalculating batting statistics...")

batting_stats = deliveries.groupby('batter').agg({
    'batsman_runs': ['sum', 'count'],
    'is_wicket': 'sum',
    'match_id': 'nunique'
}).reset_index()

batting_stats.columns = ['player', 'total_runs', 'balls_faced', 'times_out', 'matches_played']

# Calculate average (runs / times out)
batting_stats['batting_average'] = (batting_stats['total_runs'] / 
                                    batting_stats['times_out'].replace(0, np.nan)).fillna(batting_stats['total_runs'])
batting_stats['batting_average'] = batting_stats['batting_average'].round(2)

# Calculate strike rate
batting_stats['strike_rate'] = ((batting_stats['total_runs'] / batting_stats['balls_faced']) * 100).round(2)

# Calculate boundaries
boundaries = deliveries.groupby('batter').agg({
    'batsman_runs': lambda x: (x == 4).sum()
}).reset_index()
boundaries.columns = ['player', 'fours']

sixes = deliveries.groupby('batter').agg({
    'batsman_runs': lambda x: (x == 6).sum()
}).reset_index()
sixes.columns = ['player', 'sixes']

batting_stats = batting_stats.merge(boundaries, on='player').merge(sixes, on='player')

print(f"✓ Calculated batting stats for {len(batting_stats)} players")

# ===== BOWLING STATISTICS =====
print("\nCalculating bowling statistics...")

bowling_stats = deliveries.groupby('bowler').agg({
    'total_runs': 'sum',
    'is_wicket': 'sum',
    'ball': 'count',
    'match_id': 'nunique'
}).reset_index()

bowling_stats.columns = ['player', 'runs_conceded', 'wickets', 'balls_bowled', 'matches_bowled']

# Calculate economy rate (runs per over)
bowling_stats['economy_rate'] = ((bowling_stats['runs_conceded'] / 
                                  bowling_stats['balls_bowled']) * 6).round(2)

# Calculate average (runs per wicket)
bowling_stats['bowling_average'] = (bowling_stats['runs_conceded'] / 
                                    bowling_stats['wickets'].replace(0, np.nan)).round(2)

# Calculate strike rate (balls per wicket)
bowling_stats['bowling_strike_rate'] = (bowling_stats['balls_bowled'] / 
                                        bowling_stats['wickets'].replace(0, np.nan)).round(2)

print(f"✓ Calculated bowling stats for {len(bowling_stats)} players")

# ===== COMBINE AND CLASSIFY PLAYERS =====
print("\nCombining statistics and classifying players...")

# Merge batting and bowling
all_players = batting_stats.merge(bowling_stats, on='player', how='outer', suffixes=('_bat', '_bowl'))

# Fill NaN values for players who only bat or only bowl
all_players = all_players.fillna(0)

# Classify player role based on performance
def classify_role(row):
    if row['matches_played'] >= 10 and row['matches_bowled'] >= 10:
        return 'All-rounder'
    elif row['matches_played'] >= 10:
        return 'Batsman'
    elif row['matches_bowled'] >= 10:
        return 'Bowler'
    else:
        return 'Unknown'

all_players['role'] = all_players.apply(classify_role, axis=1)

# Filter players with significant participation (at least 20 matches)
all_players['total_matches'] = all_players[['matches_played', 'matches_bowled']].max(axis=1)
significant_players = all_players[all_players['total_matches'] >= 20].copy()

# Sort by total runs
significant_players = significant_players.sort_values('total_runs', ascending=False)

print(f"✓ Identified {len(significant_players)} significant players")

# Save processed data
significant_players.to_csv('data/player_statistics.csv', index=False)

print("\n" + "=" * 70)
print("PLAYER STATISTICS SUMMARY")
print("=" * 70)

print(f"\n📊 Total Significant Players: {len(significant_players)}")
print(f"\nRole Distribution:")
print(significant_players['role'].value_counts())

print(f"\n🏏 Top 10 Run Scorers:")
print(significant_players[['player', 'total_runs', 'batting_average', 'strike_rate']].head(10).to_string(index=False))

print(f"\n🎯 Top 10 Wicket Takers:")
top_bowlers = significant_players[significant_players['wickets'] > 0].sort_values('wickets', ascending=False)
print(top_bowlers[['player', 'wickets', 'economy_rate', 'bowling_average']].head(10).to_string(index=False))

print("\n" + "=" * 70)
print("✓ PROCESSING COMPLETE!")
print("=" * 70)
print("\n📁 Saved: data/player_statistics.csv")
print("=" * 70)