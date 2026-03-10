from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt


WORKSHOP_STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.color": "#e6e6e6",
    "grid.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.frameon": False,
}


def apply_workshop_style() -> None:
    mpl.rcParams.update(WORKSHOP_STYLE)


def set_seaborn_theme() -> None:
    try:
        import seaborn as sns
    except ImportError:
        return
    sns.set_theme(style="whitegrid", font_scale=1.0)


def quick_title(ax: plt.Axes, title: str, subtitle: str | None = None) -> None:
    ax.set_title(title, loc="left")
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=8, color="#555")
