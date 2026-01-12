# Sports Performance & Match Analytics Pipeline

End-to-end data pipeline for football performance analytics.
Built for semi-professional clubs with limited resources.

## What this does
- Ingests basic, match, event and load data from CSV
- Determines athletes BMI & maximum heart rate
- Calculates athletes four trainingzones
- Builds player- and match-level performance metrics
- Tracks both low-effort baseline metrics and high-resolution event data
- Generates plots and PDF-ready outputs

## Why this matters
- Immediate analytical output from trainingday 1
- System improves automatically as data grows
- Low operational overhead, high informational value

## Data
Input data is CSV-based and fully interchangeable.
Only file paths need to be adjusted.

## Example Outputs
- Training:
  - BMI classification & training zones (baseline health & conditioning)
  - RPE (Rate of Perceived Exertion) trends over time (load management & injury risk awareness)

- Match / Season:
  - Goal & goals-conceded distribution by game phase (match flow & risk windows)
  - Starting XI frequency & average minutes played (squad utilization)
  - Discipline & substitutions (in-game decision patterns)

- Player:
  - Goals & assists (per match, per 90, minutes per contribution)
  - Minutes played vs. not played (availability & usage)
  - Starts, substitutions & discipline (role stability & management)

## Tech Stack
- Python
- pandas
- matplotlib
- reportlab
- CSV

## Status
Active development. MVP-level but production-oriented.
