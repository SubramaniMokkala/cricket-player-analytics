import pandas as pd

print("=" * 70)
print("LOADING IPL DATASET")
print("=" * 70)

# Load matches data
matches_df = pd.read_csv('data/matches.csv')
print(f"\n📊 Matches Dataset: {matches_df.shape}")
print("\nColumns:", list(matches_df.columns))
print("\nSample:")
print(matches_df.head())

# Load deliveries data
deliveries_df = pd.read_csv('data/deliveries.csv')
print(f"\n📊 Deliveries Dataset: {deliveries_df.shape}")
print("\nColumns:", list(deliveries_df.columns))
print("\nSample:")
print(deliveries_df.head())

print("\n" + "=" * 70)
print("✓ DATA LOADED SUCCESSFULLY!")
print("=" * 70)