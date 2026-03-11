from __future__ import annotations

import types
from pathlib import Path
from unittest.mock import MagicMock, patch, call
import pandas as pd
import numpy as np
import pytest

import speedtrace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_telemetry(n: int = 100) -> pd.DataFrame:
    distance = np.linspace(0, 5000, n)
    return pd.DataFrame({
        "Distance": distance,
        "Speed": np.random.uniform(80, 330, n),
        "Throttle": np.random.uniform(0, 100, n),
        "Brake": np.random.randint(0, 2, n).astype(float),
        "nGear": np.random.randint(1, 9, n),
    })


def _make_lap(tel: pd.DataFrame) -> MagicMock:
    lap = MagicMock()
    car_data = MagicMock()
    car_data.add_distance.return_value = tel
    lap.get_car_data.return_value = car_data
    return lap


def _make_laps(lap1: MagicMock, lap2: MagicMock, driver1: str = "VER", driver2: str = "HAM") -> MagicMock:
    laps = MagicMock()

    def pick_drivers(drv: str) -> MagicMock:
        driver_laps = MagicMock()
        lap = lap1 if drv == driver1 else lap2
        driver_laps.pick_fastest.return_value = lap
        # Simulate pick by LapNumber
        driver_laps.__getitem__ = MagicMock(return_value=MagicMock(iloc={0: lap}))
        return driver_laps

    laps.pick_drivers.side_effect = pick_drivers
    return laps


# ---------------------------------------------------------------------------
# parse_args
# ---------------------------------------------------------------------------

def test_parse_args_positional():
    args = speedtrace.parse_args(["2024", "Monza", "Q", "VER", "HAM"])
    assert args.year == 2024
    assert args.race == "Monza"
    assert args.session == "Q"
    assert args.driver1 == "VER"
    assert args.driver2 == "HAM"
    assert args.lap is None
    assert args.save is None


def test_parse_args_optional_lap_and_save():
    args = speedtrace.parse_args(["2024", "Monza", "R", "VER", "HAM", "--lap", "30", "--save", "out.png"])
    assert args.lap == 30
    assert args.save == "out.png"


# ---------------------------------------------------------------------------
# build_plot
# ---------------------------------------------------------------------------

def test_build_plot_returns_four_subplots():
    import matplotlib
    matplotlib.use("Agg")

    tel1 = _make_telemetry()
    tel2 = _make_telemetry()
    fig = speedtrace.build_plot(tel1, tel2, "VER", "HAM", "Test Title")
    axes = fig.get_axes()
    assert len(axes) == 4


def test_build_plot_two_lines_per_panel():
    import matplotlib
    matplotlib.use("Agg")

    tel1 = _make_telemetry()
    tel2 = _make_telemetry()
    fig = speedtrace.build_plot(tel1, tel2, "VER", "HAM", "Test Title")
    axes = fig.get_axes()
    for ax in axes:
        assert len(ax.get_lines()) == 2, f"Expected 2 lines, got {len(ax.get_lines())}"


# ---------------------------------------------------------------------------
# get_lap
# ---------------------------------------------------------------------------

def test_get_lap_fastest():
    tel = _make_telemetry()
    lap = _make_lap(tel)
    driver_laps = MagicMock()
    driver_laps.pick_fastest.return_value = lap

    laps = MagicMock()
    laps.pick_drivers.return_value = driver_laps

    result = speedtrace.get_lap(laps, "VER", None)
    driver_laps.pick_fastest.assert_called_once()
    assert result is lap


def test_get_lap_by_number():
    tel = _make_telemetry()
    lap = _make_lap(tel)

    # Build a mock that supports boolean indexing via __getitem__
    filtered = MagicMock()
    filtered.iloc = {0: lap}

    driver_laps = MagicMock()
    driver_laps.__getitem__ = MagicMock(return_value=filtered)

    laps = MagicMock()
    laps.pick_drivers.return_value = driver_laps

    result = speedtrace.get_lap(laps, "VER", 30)
    assert result is lap


# ---------------------------------------------------------------------------
# main — save vs show
# ---------------------------------------------------------------------------

def _run_main_mocked(argv: list[str], tmp_path):
    """Helper: run main() with fastf1 and build_plot mocked, cwd set to tmp_path."""
    import os
    tel1, tel2 = _make_telemetry(), _make_telemetry()
    lap1, lap2 = _make_lap(tel1), _make_lap(tel2)
    mock_session = MagicMock()
    mock_session.laps = _make_laps(lap1, lap2)

    with patch("speedtrace.fastf1") as mock_fastf1, \
         patch("speedtrace.plt") as mock_plt, \
         patch("speedtrace.build_plot") as mock_build:
        mock_fastf1.get_session.return_value = mock_session
        mock_fig = MagicMock()
        mock_build.return_value = mock_fig

        orig = os.getcwd()
        os.chdir(tmp_path)
        try:
            speedtrace.main(argv)
        finally:
            os.chdir(orig)

        return mock_fig, mock_plt


def test_main_save_full_path_calls_savefig(tmp_path):
    save_path = tmp_path / "result.png"
    mock_fig, mock_plt = _run_main_mocked(
        ["2024", "Monza", "Q", "VER", "HAM", "--save", str(save_path)],
        tmp_path,
    )
    mock_fig.savefig.assert_called_once_with(save_path, dpi=150, bbox_inches="tight")
    mock_plt.show.assert_not_called()


def test_main_save_bare_filename_goes_to_output_dir(tmp_path):
    mock_fig, mock_plt = _run_main_mocked(
        ["2024", "Monza", "Q", "VER", "HAM", "--save", "result.png"],
        tmp_path,
    )
    expected = Path("output") / "result.png"
    mock_fig.savefig.assert_called_once_with(expected, dpi=150, bbox_inches="tight")
    mock_plt.show.assert_not_called()


def test_main_no_save_calls_show(tmp_path):
    mock_fig, mock_plt = _run_main_mocked(
        ["2024", "Monza", "Q", "VER", "HAM"],
        tmp_path,
    )
    mock_plt.show.assert_called_once()
    mock_fig.savefig.assert_not_called()
