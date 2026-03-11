from __future__ import annotations

import argparse
import sys
from pathlib import Path

import fastf1
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare F1 driver speed traces on a shared distance axis."
    )
    parser.add_argument("year", type=int, help="Season year (e.g. 2024)")
    parser.add_argument("race", type=str, help="Race name or round (e.g. Monza)")
    parser.add_argument(
        "session",
        type=str,
        choices=["Q", "R", "FP1", "FP2", "FP3", "SQ", "S"],
        help="Session type",
    )
    parser.add_argument("driver1", type=str, help="First driver abbreviation (e.g. VER)")
    parser.add_argument("driver2", type=str, help="Second driver abbreviation (e.g. HAM)")
    parser.add_argument(
        "--lap",
        type=int,
        default=None,
        help="Lap number to compare (default: fastest lap)",
    )
    parser.add_argument(
        "--save",
        type=str,
        default=None,
        metavar="PATH",
        help="Save plot to file instead of displaying (e.g. output.png)",
    )
    return parser.parse_args(argv)


def get_lap(laps: object, driver: str, lap_number: int | None):
    driver_laps = laps.pick_drivers(driver)
    if lap_number is None:
        return driver_laps.pick_fastest()
    return driver_laps[driver_laps["LapNumber"] == lap_number].iloc[0]


def load_telemetry(lap) -> object:
    return lap.get_car_data().add_distance()


def build_plot(
    tel1: object,
    tel2: object,
    driver1: str,
    driver2: str,
    title: str,
) -> plt.Figure:
    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(14, 10))
    fig.suptitle(title, fontsize=12, fontweight="bold")

    colors = ("#E8002D", "#00D2BE")  # red, teal
    d1_color, d2_color = colors

    # Speed
    axes[0].plot(tel1["Distance"], tel1["Speed"], color=d1_color, label=driver1)
    axes[0].plot(tel2["Distance"], tel2["Speed"], color=d2_color, label=driver2)
    axes[0].set_ylabel("Speed (km/h)")
    axes[0].legend(loc="upper right")

    # Throttle
    axes[1].plot(tel1["Distance"], tel1["Throttle"], color=d1_color, label=driver1)
    axes[1].plot(tel2["Distance"], tel2["Throttle"], color=d2_color, label=driver2)
    axes[1].set_ylabel("Throttle (%)")
    axes[1].set_ylim(-5, 105)

    # Brake (step plot)
    axes[2].step(tel1["Distance"], tel1["Brake"], color=d1_color, where="post", label=driver1)
    axes[2].step(tel2["Distance"], tel2["Brake"], color=d2_color, where="post", label=driver2, alpha=0.7)
    axes[2].set_ylabel("Brake")
    axes[2].set_ylim(-0.1, 1.2)
    axes[2].set_yticks([0, 1])

    # Gear (step plot)
    axes[3].step(tel1["Distance"], tel1["nGear"], color=d1_color, where="post", label=driver1)
    axes[3].step(tel2["Distance"], tel2["nGear"], color=d2_color, where="post", label=driver2, alpha=0.7)
    axes[3].set_ylabel("Gear")
    axes[3].set_xlabel("Distance (m)")

    fig.tight_layout()
    return fig


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    cache_dir = Path.home() / ".cache" / "fastf1"
    cache_dir.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))

    session = fastf1.get_session(args.year, args.race, args.session)
    session.load(telemetry=True, laps=True)

    laps = session.laps
    lap1 = get_lap(laps, args.driver1, args.lap)
    lap2 = get_lap(laps, args.driver2, args.lap)

    tel1 = load_telemetry(lap1)
    tel2 = load_telemetry(lap2)

    lap_label = "fastest" if args.lap is None else str(args.lap)
    title = (
        f"{args.race} {args.year} — {args.session} | "
        f"{args.driver1} vs {args.driver2} | Lap: {lap_label}"
    )

    fig = build_plot(tel1, tel2, args.driver1, args.driver2, title)

    if args.save:
        fig.savefig(args.save, dpi=150, bbox_inches="tight")
        print(f"Saved to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
