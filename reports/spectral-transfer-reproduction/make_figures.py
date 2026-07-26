#!/usr/bin/env python3
"""Build deterministic evidence figures from committed raw outputs."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)
ART = ROOT / ".openresearch" / "artifacts"
plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.hashsalt": "2606.01292",
    }
)
COLORS = {
    "navy": "#173F5F",
    "blue": "#20639B",
    "green": "#3CAEA3",
    "gold": "#F6D55C",
    "red": "#ED553B",
    "gray": "#667085",
}


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    target = OUT / name
    fig.savefig(target, format="svg", metadata={"Date": None})
    plt.close(fig)
    # Matplotlib embeds harmless trailing spaces in path definitions. Normalize
    # them so these text-only figures have stable, reviewable diffs.
    normalized = "\n".join(
        line.rstrip() for line in target.read_text().splitlines()
    )
    target.write_text(normalized + "\n")


with (ART / "claim-5" / "checkpoints.csv").open(newline="") as handle:
    checkpoints = list(csv.DictReader(handle))
summary = json.loads(
    (ART / "claim-5" / "experiment_summary.json").read_text()
)
bootstrap = json.loads((ART / "claim-5" / "bootstrap.json").read_text())

results = summary["results"]
labels = ["Teacher", "Best W2S\n(epoch 2)", "Final W2S\n(epoch 20)", "Shuffled\ncontrol"]
values = [
    results["teacher_mse"],
    results["best_w2s_mse"],
    results["final_w2s_mse"],
    results["best_control_mse"],
]
fig, ax = plt.subplots(figsize=(7.2, 3.8))
bars = ax.bar(
    labels,
    values,
    color=[COLORS["gray"], COLORS["green"], COLORS["blue"], COLORS["red"]],
    width=0.68,
)
ax.set_ylabel("UTKFace test MSE (lower is better)")
ax.set_title("A real CLIP student beats its ResNet18 teacher—and needs stopping")
ax.set_ylim(0, max(values) * 1.18)
for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 8,
        f"{value:.1f}",
        ha="center",
        fontweight="bold",
    )
ci = results["bootstrap"]["teacher_minus_best_w2s"]
ax.text(
    0.5,
    max(values) * 1.09,
    f"Teacher − best W2S = {ci['mean_difference']:.1f}, "
    f"95% CI [{ci['ci95_low']:.1f}, {ci['ci95_high']:.1f}]",
    ha="center",
    color=COLORS["navy"],
)
save(fig, "01_headline_real_w2s.svg")

epochs = [int(row["epoch"]) for row in checkpoints]
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(
    epochs,
    [float(row["w2s_mse"]) for row in checkpoints],
    marker="o",
    markersize=3,
    label="W2S pseudolabels",
    color=COLORS["green"],
)
ax.plot(
    epochs,
    [float(row["direct_mse"]) for row in checkpoints],
    label="Direct labels (ceiling)",
    color=COLORS["blue"],
)
ax.plot(
    epochs,
    [float(row["shuffled_control_mse"]) for row in checkpoints],
    label="Shuffled pseudolabel control",
    color=COLORS["red"],
    alpha=0.78,
)
ax.axhline(results["teacher_mse"], label="Teacher", color=COLORS["gray"], linestyle="--")
ax.axvline(results["best_w2s_epoch"], color=COLORS["gold"], linewidth=3, alpha=0.8)
ax.annotate(
    "best W2S: epoch 2",
    (2, results["best_w2s_mse"]),
    xytext=(5, 160),
    arrowprops={"arrowstyle": "->", "color": COLORS["navy"]},
)
ax.set_xlabel("Linear-head epoch")
ax.set_ylabel("Test MSE")
ax.set_title("The W2S optimum is intermediate, not the final checkpoint")
ax.set_xticks([1, 2, 5, 10, 15, 20])
ax.legend(frameon=False, ncol=2)
save(fig, "02_early_stopping_curve.svg")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.7))
ax1.plot(
    epochs,
    [float(row["PGR_using_best_direct_ceiling"]) for row in checkpoints],
    color=COLORS["green"],
    marker="o",
    markersize=3,
)
ax1.axvline(2, color=COLORS["gold"], linewidth=3, alpha=0.8)
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Performance gap recovered")
ax1.set_title("PGR peaks early")
ax1.set_ylim(0.72, 0.86)
ax2.plot(
    epochs,
    [int(row["projection_k80"]) for row in checkpoints],
    color=COLORS["blue"],
    marker="o",
    markersize=3,
)
ax2.axhline(29, color=COLORS["gold"], linestyle="--")
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Dimensions for 80% head energy")
ax2.set_title("Spectral spread")
save(fig, "03_pgr_and_projection.svg")

with (ART / "claim-3" / "independent_horizon_audit.csv").open(
    newline=""
) as handle:
    claim3 = list(csv.DictReader(handle))
fig, ax = plt.subplots(figsize=(7.2, 3.8))
ax.loglog(
    [int(row["n"]) for row in claim3],
    [float(row["student_minus_teacher"]) for row in claim3],
    marker="o",
    color=COLORS["red"],
)
ax.axhline(0, color="black", linewidth=1)
ax.set_xlabel("Student horizon n")
ax.set_ylabel("Expected risk gap: student − teacher")
ax.set_title("Theorem 4 counterexample stays above zero at every finite horizon")
ax.text(
    0.04,
    0.08,
    "Exact algebra proves positivity for all finite n;\n"
    "points are an independent 80-digit audit.",
    transform=ax.transAxes,
    color=COLORS["navy"],
)
save(fig, "04_theorem4_counterexample.svg")

with (ART / "claim-4" / "independent_cutoff_sweep.csv").open(
    newline=""
) as handle:
    claim4 = list(csv.DictReader(handle))
fig, ax = plt.subplots(figsize=(7.2, 3.8))
for route, color, label in (
    ("theorem", COLORS["red"], "Theorem's stated n exponent"),
    ("reconstructed", COLORS["green"], "Exponent required by its cutoff lemma"),
):
    rows = [row for row in claim4 if row["route"] == route]
    ax.plot(
        [int(row["log10_N"]) for row in rows],
        [float(row["effective_cutoff_logN_slope"]) for row in rows],
        marker="o",
        color=color,
        label=label,
    )
ax.axhline(0.1, color=COLORS["navy"], linestyle="--", label="Advertised cutoff slope 0.10")
ax.axhline(0.05, color=COLORS["gray"], linestyle=":", label="Stated route limit 0.05")
ax.set_xlabel("log10(N)")
ax.set_ylabel("Effective log(k*) / log(N)")
ax.set_title("Theorem 5 maps its stopping horizon to the wrong cutoff rate")
ax.legend(frameon=False)
save(fig, "05_theorem5_rate_mismatch.svg")

print(f"wrote {len(list(OUT.glob('*.svg')))} deterministic SVG figures to {OUT}")
