# Formula 1 Data Analysis Primer

A reference guide to the publicly available F1 data APIs and what the community is building with them.

---

## Public APIs

### [FastF1](https://github.com/theOehrly/Fast-F1) *(Python — most feature-rich)*
```bash
pip install fastf1
```
- Parses the official F1 live timing stream — no API key required
- Lap-by-lap telemetry: speed, throttle, brake, gear, DRS, RPM
- Car positional data (X/Y/Z coordinates)
- Tyre compound and stint data
- Weather data per session
- Driver radio messages
- Covers 2018–present (partial 2014–2017)
- Returns data as extended Pandas DataFrames

### [OpenF1](https://openf1.org/) *(REST API — Python or Swift)*
- Free, open-source, no auth required
- ~3 second latency behind live events
- 18 endpoints: car data, lap data, intervals, stints, pit stops, race control messages
- JSON (default) or CSV output (`?csv=true`)
- Covers 2023–present
- Rate limit: 3 req/sec, 30 req/min (free tier)
- Community Python SDK: [rhtnr/OpenF1-python-client](https://github.com/rhtnr/OpenF1-python-client)

### [Jolpica F1 API](https://api.jolpi.ca/ergast/) *(Ergast successor)*
- Historical data back to 1950
- Race results, standings, lap times, pit stops, circuits, drivers, constructors
- REST/JSON — works from any language including Swift

---

## Data Categories

| Category | FastF1 | OpenF1 | Jolpica/Ergast |
|---|---|---|---|
| Telemetry (speed, throttle, etc.) | Yes | Yes (2023+) | No |
| Lap times | Yes | Yes | Yes (1950+) |
| Pit stops | Yes | Yes | Yes |
| Standings | No | No | Yes |
| Historical data (pre-2018) | Limited | No | Yes |
| Live session data | Yes | Yes | No |
| Tyre/stint data | Yes | Yes | No |
| Weather | Yes | No | No |
| Driver radio | Yes | Yes | No |

---

## What the Community is Building

### 1. Driver Telemetry Comparisons
The most common entry point. Load two drivers' fastest laps and overlay speed, throttle, brake, and gear traces on a shared distance axis.

- Speed traces with corner annotations
- Throttle/brake application overlays
- Gear change heatmaps on circuit maps
- Recreation of the AWS Corner Analysis broadcast graphic (classifying Full Throttle / Braking / Cornering and colouring a circuit map)
  - Example: [mosesmulwa-bebop/F1-AWS-Corner-Analysis-in-Python](https://github.com/mosesmulwa-bebop/F1-AWS-Corner-Analysis-in-Python)

### 2. Race Strategy & Tyre Visualizations
Stacked bar charts showing each driver's stint lengths and tyre compounds, plus lap time degradation curves.

- Stint length vs. tyre compound per driver per race
- Lap time delta graphs showing degradation cliffs
- Full-grid strategy comparison charts
- Example: [ZainMirza-2004/F1-Tyre-Degradation-Simulation](https://github.com/ZainMirza-2004/F1-Tyre-Degradation-Simulation)

### 3. Machine Learning Race Prediction

| Prediction Target | Typical Model | Notes |
|---|---|---|
| Pit stop window | XGBoost, Random Forest | One student hit 83% accuracy live on Twitch |
| Tyre degradation cliff | XGBoost | Best reported: ~1.7 lap mean error |
| Qualifying lap time | Deep Neural Network | Outperforms polynomial regression on nonlinear inputs |
| Race result / podium | Ensemble stacking, GBM | One project: 89.5% accuracy across 21 races |

Examples:
- [aniketh05/formula-1-pit-stop-prediction](https://github.com/aniketh05/formula-1-pit-stop-prediction) — stacking classifier (RF + SVC + GBM)
- [jaeyow/f1-predictor](https://github.com/jaeyow/f1-predictor) — end-to-end with GitHub Actions as MLOps pipeline
- [sidgaikwad07/F1_tire_degradation_strategy_predictor](https://github.com/sidgaikwad07/F1_tire_degradation_strategy_predictor)

### 4. Reinforcement Learning Strategy Simulators
Treat pit stop timing as a sequential decision problem and train an RL agent to find optimal windows.

- [rembertdesigns/pit-stop-simulator](https://github.com/rembertdesigns/pit-stop-simulator) — PPO + Q-Learning via stable-baselines3, Streamlit front-end
- Compound-specific wear models: Soft 1.5× / Medium 1.0× / Hard 0.7× base wear rate
- Academic work using Bi-LSTM (precision 0.77, recall 0.86, F1-score 0.81)

### 5. Interactive Live Timing Dashboards
- [f1-dash.com](https://f1-dash.com) / [slowlydev/f1-dash](https://github.com/slowlydev/f1-dash) — real-time leaderboard, sector times, gaps, tyre choices. Open source, hobby project started 2023.
- [FraserTarbet/F1Dash](https://github.com/FraserTarbet/F1Dash) — track sector map coloured by fastest driver, side-by-side telemetry, lap time scatter

### 6. Driving Style Clustering
Unsupervised ML to characterize driver behaviour across sessions.

- KNN/clustering on braking zone selection, throttle aggression, cornering consistency
- Detects anomalous laps (safety cars, VSCs) automatically from lap time data
- Streamlit apps comparing any two drivers across behavioral dimensions
- Reference: ["Visualising and clustering racing patterns"](https://medium.com/the-everyday-academic/visualising-and-clustering-racing-patterns-9e6c94f98ac7)

### 7. Historical & Statistical Analysis
Using Jolpica/Ergast (1950–present) rather than FastF1.

- GOAT analysis (Hamilton vs Schumacher vs Senna by win%, podium%, championship-adjusted metrics)
- Championship points trajectory animations
- Constructor longevity and name-change timelines (Gantt charts)
- Sentiment analysis of r/formula1 race threads correlated with race ratings
- Example: [PiotrMajor/F1-Data-Visualization](https://github.com/PiotrMajor/F1-Data-Visualization)

### 8. Full Data Engineering Pipelines
F1 as a learning platform for data engineering:

- Python → dbt → PostgreSQL: ["Zero Lap to Hero"](https://blog.dataengineerthings.org/zero-lap-to-hero-building-a-formula-1-analytics-stack-with-python-dbt-and-postgres-f41409c79b6c)
- AWS Glue + Athena + S3 + Streamlit: [frankndungu/f1-streamlit-data-pipline](https://github.com/frankndungu/f1-streamlit-data-pipline)
- Azure Databricks + Delta Lake + ADF lakehouse: [Muhyd33n/Formula1RacingProject](https://github.com/Muhyd33n/Formula1RacingProject)

---

## Common Tech Stack

| Layer | Tools |
|---|---|
| Data access | FastF1, OpenF1, Jolpica/Ergast |
| Data manipulation | Pandas, NumPy |
| ML / statistics | Scikit-learn, XGBoost, statsmodels |
| Deep learning | TensorFlow/Keras, PyTorch (GRU/LSTM) |
| RL | stable-baselines3, Gymnasium |
| Visualization | Matplotlib, Plotly, Seaborn |
| Web apps | Streamlit, Dash, Flask |
| Data engineering | dbt, AWS Glue/Athena, Azure Databricks |
| Notebooks | Jupyter, Google Colab |

---

## Community Resources

| Resource | What it offers |
|---|---|
| [medium.com/towards-formula-1-analysis](https://medium.com/towards-formula-1-analysis) | Largest tutorial publication, beginner to advanced with full code |
| [racingdatalab.com](https://www.racingdatalab.com) | Google Colab notebooks, no local setup needed |
| [tracinginsights.com](https://tracinginsights.com) | No-code web tool for sector/lap analysis |
| [github.com/topics/fastf1](https://github.com/topics/fastf1) | Community project discovery |
| [github.com/topics/formula1-analysis](https://github.com/topics/formula1-analysis) | More community projects |

---

## Getting Started (5-minute version)

```python
import fastf1
from matplotlib import pyplot as plt

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2024, 'Monza', 'Q')
session.load()

ver = session.laps.pick_driver('VER').pick_fastest().get_car_data().add_distance()
ham = session.laps.pick_driver('HAM').pick_fastest().get_car_data().add_distance()

fig, ax = plt.subplots()
ax.plot(ver['Distance'], ver['Speed'], label='Verstappen')
ax.plot(ham['Distance'], ham['Speed'], label='Hamilton')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Speed (km/h)')
ax.legend()
plt.show()
```
