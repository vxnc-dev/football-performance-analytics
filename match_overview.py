import pandas as pd
import os

# CSVs laden
MATCH_LOAD_PATH = r"" #MATCH_LOAD.CSV
MATCHES_PATH = r"" #MATCHES.CSV
SAVE_PATH = None

matches_df = pd.read_csv(MATCHES_PATH)
match_load_df = pd.read_csv(MATCH_LOAD_PATH)

# Typen erzwingen
matches_df["match_id"] = matches_df["match_id"].astype(int)
match_load_df["match_id"] = match_load_df["match_id"].astype(int)
match_load_df["player_id"] = match_load_df["player_id"].astype(int)
match_load_df["minutes_played"] = match_load_df["minutes_played"].astype(int)
match_load_df["sub"] = match_load_df["sub"].astype(bool)

def build_match_overview(matches_df, match_load_df):
	# Team-Metriken pro Spiel
	team_stats = (
		match_load_df
		.groupby("match_id", as_index=False)
		.agg(
			players_used=("player_id", "nunique"),
			avg_minutes=("minutes_played", "mean"),
			subs_used=("sub", "sum")
		)
	)
	team_stats["avg_minutes"] = team_stats["avg_minutes"].round(2)

	# Mit Match-Infos verheiraten
	overview = matches_df.merge(
		team_stats,
		on="match_id",
		how="left"
	)

	# Aufräumen
	overview["subs_used"] = overview["subs_used"].fillna(0).astype(int)
	overview["players_used"] = overview["subs_used"] + 11

	return overview.sort_values("date").reset_index(drop=True)

# Usage
match_overview_df = build_match_overview(matches_df, match_load_df)

if SAVE_PATH is None:
		save_dir = r"" #PATH TO DATA_PROCESSED
		os.makedirs(save_dir, exist_ok=True)
		save_path = os.path.join(save_dir, "match_overview.csv")
match_overview_df.to_csv(save_path, index=False)
print("Saved at: " + save_path)

