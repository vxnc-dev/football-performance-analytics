import pandas as pd
from datetime import datetime
import os

def enrich_and_save_player_master(df, save_path=None):
	today = datetime.today().date()

	def _calc_age(born_str):
		b = datetime.strptime(born_str, "%Y-%m-%d").date()
		age = today.year - b.year
		if (today.month, today.day) < (b.month, b.day):
			age -= 1
		return age

	def add_bmi(df, weight_col="weight_kg", height_col="height_cm", bmi_col="bmi", category_col="bmi_category"):
		df[bmi_col] = (df[weight_col] / (df[height_col]/100)**2).round(1)
		
		def categorize(bmi):
			if bmi < 18.5:
				return "underweight"
			elif 18.5 <= bmi < 25:
				return "normal weight"
			elif 25 <= bmi < 30:
				return "overweight"
			else:
				return "obese"

		df[category_col] = df[bmi_col].apply(categorize)
		return df

	df['age'] = df['born'].apply(_calc_age)
	df = add_bmi(df)

	df['hr_max'] = (
		214
		- 0.5 * df['age']
		- 0.11 * df['weight_kg']
	).round().astype(int) # SALLY-EDWARDS

	df['bmr'] = (10 * df['weight_kg'] + (6.25 * df['height_cm']) - (5 * df['age']) + 5).round().astype(int)
	df['EBedarf'] = (df['bmr'] * 1.55).round().astype(int) #  *1.55 -> moderate activity; 3-5x/Week active

	df['Zone 1 light zone'] = df['hr_max'].apply(lambda x: f"{int(round(0.5*x))}-{int(round(0.6*x))}")
	df['Zone 2 fat burning zone'] = df['hr_max'].apply(lambda x: f"{int(round(0.6*x))}-{int(round(0.7*x))}")
	df['Zone 3 aerobic zone'] = df['hr_max'].apply(lambda x: f"{int(round(0.7*x))}-{int(round(0.8*x))}")
	df['Zone 4 anaerobic zone'] = df['hr_max'].apply(lambda x: f"{int(round(0.8*x))}-{int(round(0.9*x))}")
	df['Zone 5 maximum effort'] = df['hr_max'].apply(lambda x: f"{int(round(0.9*x))}-{int(round(0.95*x))}")


	if save_path is None:
		save_dir = r"" # DATA_PROCESSED PATH
		os.makedirs(save_dir, exist_ok=True)
		save_path = os.path.join(save_dir, "squad_enrichment.csv")

	df.to_csv(save_path, index=False)
	print(f"Data Enrichment saved at: {save_path}")
	return df

df_path = r"" # SQUAD.CSV PATH
df = pd.read_csv(df_path)
df = enrich_and_save_player_master(df)