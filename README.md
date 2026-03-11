# FormulaUn
Goofin.

## Scripts

### `speedtrace.py` — Driver Speed Trace Comparison

Compare two F1 drivers' telemetry (speed, throttle, brake, gear) on a shared distance axis using FastF1.

#### Setup

```bash
pip install -r requirements.txt
```

FastF1 data is cached at `~/.cache/fastf1` on first run (~50 MB per session).

#### Usage

```bash
# Fastest lap comparison — qualifying
python speedtrace.py 2024 Monza Q VER LEC

# Specific lap — race
python speedtrace.py 2024 Monza R VER HAM --lap 30

# Save to PNG instead of displaying
python speedtrace.py 2024 Monza Q VER LEC --save monza_q.png
```

#### Arguments

| Argument | Type | Description |
|---|---|---|
| `year` | int | Season year (e.g. `2024`) |
| `race` | str | Race name or round (e.g. `Monza`, `1`) |
| `session` | str | Session type: `Q`, `R`, `FP1`, `FP2`, `FP3`, `SQ`, `S` |
| `driver1` | str | First driver abbreviation (e.g. `VER`) |
| `driver2` | str | Second driver abbreviation (e.g. `HAM`) |
| `--lap N` | int | Lap number (default: fastest lap) |
| `--save PATH` | str | Save plot to file (default: interactive window) |

#### Running Tests

```bash
pytest tests/ -v
```
