import pandas as pd
import matplotlib.pyplot as plt
import os

MATCH_LOAD_PATH = r"" #MATCH_LOAD.CSV
MATCHES_PATH = r"" #MATCHES.CSV
EVENTS_PATH = r"" #MATCH_EVENTS.CSV


matches_df = pd.read_csv(MATCHES_PATH)
events_df = pd.read_csv(EVENTS_PATH)
match_load_df = pd.read_csv(MATCH_LOAD_PATH)
save_path = None

events_df["minute"] = events_df["minute"].astype(int)

def build_match_summary(matches_df, events_df):
	summaries = []

	for _, match in matches_df.iterrows():
		match_id = match["match_id"]
		match_events = events_df[events_df["match_id"] == match_id]
		match_load = match_load_df[match_load_df["match_id"] == match_id]
		subs_count = match_load["sub"].sum()

		summary = {
			"match_id": match_id,
			"date": match["date"],
			"opponent": match["opponent"],
			"home_flag": match["home_flag"],
			"goals": (match_events["event_type"] == "goal").sum(),
			"assists": (match_events["event_type"] == "assist").sum(),
			"goals_against": (match_events["event_type"] == "goal_against").sum(),
			"yellow_cards": (match_events["event_type"] == "yellow_card").sum(),
			"red_cards": (match_events["event_type"] == "red_card").sum(),
			"subs": subs_count,
			"first_goal_min": match_events.loc[
			match_events["event_type"] == "goal", "minute"
			].min(),
			"last_goal_min": match_events.loc[
				match_events["event_type"] == "goal", "minute"
			].max(),
		}

		for start, end in [(0,15), (16,30), (31,45), (46,60), (61,75), (76,90), (91,99)]:
			key = f"goals_{start}_{end}"
			summary[key] = match_events[
				(match_events["event_type"] == "goal") &
				(match_events["minute"].between(start, end))
			].shape[0]
		
		for start, end in [(0,15), (16,30), (31,45), (46,60), (61,75), (76,90), (91,99)]:
			key = f"goals_conceded_{start}_{end}"
			summary[key] = match_events[
				(match_events["event_type"] == "goal_against") &
				(match_events["minute"].between(start, end))
			].shape[0]

		summaries.append(summary)

	return pd.DataFrame(summaries)

match_summary_df = build_match_summary(matches_df, events_df)
if save_path is None:
		save_dir = r"" #PATH TO DATA_PROCESSED
		os.makedirs(save_dir, exist_ok=True)
		save_path = os.path.join(save_dir, "match_summary.csv")
match_summary_df.to_csv(save_path, index=False)
print("Saved at: " + save_path)

def plot_goal_distribution_by_phase(match_summary_df):
	phase_columns = [
		"goals_0_15",
		"goals_16_30",
		"goals_31_45",
		"goals_46_60",
		"goals_61_75",
		"goals_76_90",
		"goals_91_99"
	]

	# Validation
	missing = [col for col in phase_columns if col not in match_summary_df.columns]
	if missing:
		raise ValueError(f"Missing Columns: {missing}")

	# Aggregation
	goals_by_phase = match_summary_df[phase_columns].sum()

	phase_labels = [
	"0–15",
	"16–30",
	"31–45",
	"46–60",
	"61–75",
	"76–90",
	"90+"
]

	# Plot
	plt.figure(figsize=(10, 5))
	goals_by_phase.plot(kind="bar")
	plt.title("Goal Distribution per Phase")
	plt.xlabel("Phase (Minute)")
	plt.ylabel("Goals Sum")
	plt.xticks(
	range(len(phase_labels)),
	phase_labels,
	rotation=0,
	ha="center"
	)
	plt.tight_layout()
	plt.show()

	return goals_by_phase

goals_by_phase = plot_goal_distribution_by_phase(match_summary_df)
print(goals_by_phase)

def plot_goals_conceded_distribution_by_phase(match_summary_df):
	phase_columns = [
		"goals_conceded_0_15",
		"goals_conceded_16_30",
		"goals_conceded_31_45",
		"goals_conceded_46_60",
		"goals_conceded_61_75",
		"goals_conceded_76_90",
		"goals_conceded_91_99"
	]

	# Validation
	missing = [col for col in phase_columns if col not in match_summary_df.columns]
	if missing:
		raise ValueError(f"Fehlende Spalten: {missing}")

	# Aggregation
	conceded_by_phase = match_summary_df[phase_columns].sum()

	phase_labels = [
	"0–15",
	"16–30",
	"31–45",
	"46–60",
	"61–75",
	"76–90",
	"90+"
]

	plt.figure(figsize=(10, 5))
	plt.bar(range(len(conceded_by_phase)), conceded_by_phase.values)
	conceded_by_phase.plot(kind="bar")
	plt.title("Goals against by Phase")
	plt.xlabel("Phase (Minute)")
	plt.ylabel("Goals against Sum")
	plt.xticks(
	range(len(phase_labels)),
	phase_labels,
	rotation=0,
	ha="center"
	)
	plt.tight_layout()
	plt.show()

	return conceded_by_phase

conceded_by_phase = plot_goals_conceded_distribution_by_phase(match_summary_df)
print(conceded_by_phase)