"""Draw the Coinage stress metrics charts from metrics.json.

Run: python make_charts.py  (needs matplotlib; writes the SVG files next to this script)
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = Path(__file__).parent
DATA = json.loads((HERE / "metrics.json").read_text())

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BLUE = "#2a78d6"  # finality, or the only series
ORANGE = "#eb6834"  # readiness, or the second series
GREY = "#b9b8b1"  # failed or incomplete

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "coinage-stress-metrics",
        "font.family": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "text.color": INK,
        "axes.labelcolor": INK_2,
        "axes.edgecolor": AXIS,
        "axes.facecolor": SURFACE,
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "xtick.labelcolor": INK_2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
    }
)


def fmt_s(v):
    return f"{v:,.0f} s" if v >= 100 else f"{v:,.1f} s"


def style_hbar(ax, xmax):
    ax.set_xlim(0, xmax)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()


def label_bar(ax, y, value, text, xmax, colour=INK):
    ax.text(value + xmax * 0.01, y, text, va="center", ha="left", fontsize=9, color=colour)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def lifecycle(case):
    for item in DATA["lifecycle"]:
        if item["verifiedOutcome"]["case"] == case:
            return item
    raise KeyError(case)


def wave_p95(case, suffix):
    for wave in lifecycle(case)["measurements"]["waves"]:
        if wave["name"].endswith(suffix):
            return wave["finalitySeconds"]["p95"]
    return None


def grouped_hbar(ax, rows, series, xmax, unit_fmt=fmt_s):
    """rows: list of (label, [value or None per series], [status text or None per series], faded)."""
    height = 0.8 / len(series)
    for i, (label, values, notes, faded) in enumerate(rows):
        for j, (name, colour) in enumerate(series):
            value = values[j]
            y = i - 0.4 + height * (j + 0.5)
            if value is None:
                label_bar(ax, y, 0, notes[j] or "no data", xmax, MUTED)
                continue
            ax.barh(
                y,
                value,
                height=height - 0.06,
                color=GREY if faded else colour,
                hatch="////" if faded else None,
                edgecolor=SURFACE,
                linewidth=0,
            )
            text = unit_fmt(value) + (f"  ({notes[j]})" if notes[j] else "")
            label_bar(ax, y, value, text, xmax, INK_2 if faded else INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    style_hbar(ax, xmax)


# Figure 1: top-up finality and readiness.
def topup_timing():
    earlier = DATA["earlierPublishedResults"]["topups"]
    recon = {t["run"]: t for t in DATA["topupReconciliation"]}
    r1, r2, r3 = recon[36537079387], recon[36619415692], recon[36662212241]
    rows = [
        ("1,000 at once\ndefault pool", [earlier[0]["finalityP95Seconds"], earlier[0]["readinessP95Seconds"]], [None, None], False),
        ("7,000 + 3,000 in waves\ndefault pool", [earlier[1]["finalityP95Seconds"], earlier[1]["readinessP95Seconds"]], [None, None], False),
        ("10,000 at once\nbigger pool (11,000)", [earlier[2]["finalityP95Seconds"], earlier[2]["readinessP95Seconds"]], [None, None], False),
        ("8,400 + 1,600 in waves\ndefault pool", [r3["originalFinalitySeconds"]["p95"], r3["originalReadinessSeconds"]["p95"]], [None, None], False),
        (
            "FAILED: 10,000 at once\ndefault pool",
            [r1["originalFinalitySeconds"]["p95"], r1["originalReadinessSeconds"]["p95"]],
            [f"{r1['originalFinalitySeconds']['count']:,} timed", f"{r1['originalReadinessSeconds']['count']:,} timed"],
            True,
        ),
        (
            "FAILED: 8,500 + 1,500 in waves\ndefault pool",
            [r2["originalFinalitySeconds"]["p95"], r2["originalReadinessSeconds"]["p95"]],
            [f"{r2['originalFinalitySeconds']['count']:,} timed", f"{r2['originalReadinessSeconds']['count']:,} timed"],
            True,
        ),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    grouped_hbar(ax, rows, [("Finality", BLUE), ("Readiness", ORANGE)], 460)
    ax.set_xlabel("Seconds for 95% of top-ups (p95). Shorter is better.")
    ax.set_title("Top-ups: time to settle (finality) and time to use (readiness)")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Finality p95: payment is settled"),
            Patch(color=ORANGE, label="Readiness p95: voucher can be unloaded"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Failed run (timed part only)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "topup-timing.svg")


# Figure 2: recycling finality and readiness.
def recycling_timing():
    cases = [
        ("b100", "100 at once\ndefault pool"),
        ("b1000", "1,000 at once\ndefault pool"),
        ("b_paced", "8,000 + 2,000 in waves\ndefault pool"),
        ("b_pool", "10,000 at once\nbigger pool (11,000)"),
        ("b20000", "20,000 at once\nbigger pool (22,000)"),
        ("b40000", "40,000 at once\nbigger pool (44,000)"),
        ("b10000", "INCOMPLETE: 10,000 at once\ndefault pool"),
        ("b100000", "INCOMPLETE: 100,000 at once\nbigger pool (110,000)"),
    ]
    rows = []
    for case, label in cases:
        m = lifecycle(case)["measurements"]
        incomplete = lifecycle(case)["verifiedOutcome"]["outcome"] == "incomplete"
        if case == "b_paced":
            # Wave 1 (8,000) is the slower wave and holds most of the actors.
            finality = wave_p95(case, "wave-1-recycle")
        else:
            finality = m["waves"][0]["finalitySeconds"]["p95"]
        readiness = m["readinessSeconds"]
        notes = [None, None]
        if incomplete:
            actors = lifecycle(case)["verifiedOutcome"]["requestedActors"]
            notes = [
                f"{m['waves'][0]['finalitySeconds']['count']:,} of {actors:,} timed",
                f"{readiness['count']:,} of {actors:,} seen",
            ]
        rows.append((label, [finality, readiness["p95"]], notes, incomplete))
    fig, ax = plt.subplots(figsize=(8.6, 6.8))
    grouped_hbar(ax, rows, [("Finality", BLUE), ("Readiness", ORANGE)], 2500)
    ax.set_xlabel("Seconds for 95% of recycled coins (p95). Shorter is better.")
    ax.set_title("Recycling: time to settle (finality) and time to use (readiness)")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Finality p95: load is settled"),
            Patch(color=ORANGE, label="Readiness p95: coin is in a ring root"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Incomplete run (observed part only)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "recycling-timing.svg")


# Figure 3: claim finality spread (p50, p95, p99).
def claim_finality():
    labels = ["20,000 claims", "40,000 claims", "100,000 claims"]
    fig, ax = plt.subplots(figsize=(8.6, 2.9))
    for i, item in enumerate(DATA["claimCapacityDerived"]):
        s = item["clientObservedSeconds"]["receiptLookup"]
        ax.plot([s["p50"], s["p99"]], [i, i], color=AXIS, linewidth=2, zorder=1)
        ax.scatter([s["p50"]], [i], s=70, color=SURFACE, edgecolor=BLUE, linewidth=2, zorder=3)
        ax.scatter([s["p95"]], [i], s=70, color=BLUE, edgecolor=SURFACE, linewidth=1.5, zorder=3)
        ax.scatter([s["p99"]], [i], s=70, marker="D", color=INK_2, edgecolor=SURFACE, linewidth=1.5, zorder=3)
        ax.text(s["p50"], i - 0.28, f"p50 {s['p50']:.0f} s", ha="center", fontsize=9, color=INK_2)
        ax.text(s["p99"] + 9, i, f"p95 {s['p95']:.0f} s · p99 {s['p99']:.0f} s", va="center", fontsize=9)
    ax.set_yticks(range(3), labels)
    ax.set_ylim(2.6, -0.6)
    ax.set_xlim(0, 420)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Seconds from submit to settled claim")
    ax.set_title("Claims: how long did the slowest claims wait?")
    ax.legend(
        handles=[
            plt.Line2D([], [], marker="o", linestyle="", markerfacecolor=SURFACE, markeredgecolor=BLUE, markeredgewidth=2, markersize=8, label="p50 (half were faster)"),
            plt.Line2D([], [], marker="o", linestyle="", color=BLUE, markersize=8, label="p95"),
            plt.Line2D([], [], marker="D", linestyle="", color=INK_2, markersize=7, label="p99"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.28),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "claim-finality.svg")


# Figure 4: ready queue over time.
def pool():
    titles = ["20,000 claims", "40,000 claims", "100,000 claims"]
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 8.2), sharex=True)
    for ax, item, title in zip(axes, DATA["claimCapacityDerived"], titles):
        samples = item["readyPoolSamples"]
        t = [s["secondsFromBurstStart"] for s in samples]
        for node, colour, name in [("Collator-1502", BLUE, "Collator 1"), ("Collator-1502-2", ORANGE, "Collator 2")]:
            v = [s["readyTransactions"][node] for s in samples]
            ax.plot(t, v, color=colour, linewidth=2, label=name)
            peak = max(v)
            tp = t[v.index(peak)]
            ax.annotate(f"peak {peak:,.0f}", (tp, peak), xytext=(6, 2), textcoords="offset points", fontsize=9, color=INK)
        empty = next(
            s["secondsFromBurstStart"]
            for s in samples
            if s["secondsFromBurstStart"] > 10 and all(n == 0 for n in s["readyTransactions"].values())
        )
        ax.axvline(empty, color=MUTED, linewidth=1)
        ax.text(empty + 4, ax.get_ylim()[1] * 0.55, f"both empty\nat ~{empty:.0f} s", fontsize=9, color=INK_2)
        ax.set_title(title)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.set_ylim(bottom=0)
        ax.set_ylabel("Claims waiting")
    axes[0].legend(loc="upper right", frameon=False, fontsize=9)
    axes[-1].set_xlabel("Seconds since the burst started")
    axes[-1].set_xlim(0, 340)
    fig.tight_layout()
    save(fig, "pool.svg")


# Figure 5: claims per block.
def blocks():
    titles = ["20,000 claims", "40,000 claims", "100,000 claims"]
    exps = DATA["claimCapacity"]["experiments"]
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 7.4), sharey=True)
    for ax, exp, title in zip(axes, exps, titles):
        counts = [c for _, c in sorted(exp["receiptCountsByBlock"].items(), key=lambda kv: int(kv[0]))]
        full = max(counts)
        xs = range(1, len(counts) + 1)
        ax.bar(xs, counts, width=0.8, color=[BLUE if c == full else GREY for c in counts], linewidth=0)
        ax.axhline(full, color=INK, linewidth=1)
        nfull = sum(c == full for c in counts)
        ax.text(0.4, full + 120, f"{full:,} claims in every full block ({nfull} full blocks)", fontsize=9, color=INK)
        ax.text(len(counts), counts[-1] + 80, f"{counts[-1]:,}", ha="center", fontsize=9, color=INK_2)
        ax.set_title(f"{title}: {len(counts)} blocks")
        ax.set_xlim(0.3, len(counts) + 0.7)
        ax.set_ylim(0, 3000)
        ax.set_yticks([0, 1000, 2000], ["0", "1,000", "2,000"])
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_ylabel("Claims in block")
        step = 1 if len(counts) <= 20 else 5
        ax.set_xticks([x for x in xs if x == 1 or x % step == 0])
    axes[-1].set_xlabel("Block in the run (1 = first block with workload claims)")
    fig.tight_layout()
    save(fig, "blocks.svg")


# Figure 6: split-and-claim finality.
def split_claim_timing():
    cases = [
        ("a100", "100 actors at once\ndefault pool"),
        ("a1000", "1,000 actors at once\ndefault pool"),
        ("a_paced", "8,000 + 2,000 in waves\ndefault pool (first wave)"),
        ("a_pool", "10,000 actors at once\nbigger pool (11,000)"),
        ("a20000", "LAUNCH TOO SLOW: 20,000\nbigger pool (22,000)"),
        ("a40000", "40,000 actors at once\nbigger pool (44,000)"),
        ("a100000", "100,000 actors at once\nbigger pool (110,000)"),
        ("a10000", "INCOMPLETE: 10,000 at once\ndefault pool"),
    ]
    rows = []
    for case, label in cases:
        outcome = lifecycle(case)["verifiedOutcome"]["outcome"]
        if case == "a_paced":
            split, claim = wave_p95(case, "wave-1-split"), wave_p95(case, "wave-1-claim")
        else:
            split, claim = wave_p95(case, "-split"), wave_p95(case, "-claim")
        notes = [None, None]
        if case == "a10000":
            notes = ["8,192 of 10,000 timed", "claims not sent"]
        rows.append((label, [split, claim], notes, outcome != "workload-pass"))
    fig, ax = plt.subplots(figsize=(8.6, 6.8))
    grouped_hbar(ax, rows, [("Split", BLUE), ("Claim", ORANGE)], 480)
    ax.set_xlabel("Seconds for 95% of extrinsics to settle (finality p95). Shorter is better.")
    ax.set_title("Split-and-claim: time to settle each step")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Split p95"),
            Patch(color=ORANGE, label="Claim p95"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Not a workload pass"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "split-claim-timing.svg")


# Figure 7: lifecycle completion (verified / requested extrinsics).
def completion():
    order = ["a100", "a1000", "a_paced", "a_pool", "a20000", "a40000", "a100000", "a10000",
             "b100", "b1000", "b_paced", "b_pool", "b20000", "b40000", "b10000", "b100000"]
    names = {
        "a100": "Split-and-claim, 100",
        "a1000": "Split-and-claim, 1,000",
        "a_paced": "Split-and-claim, 10,000 in waves",
        "a_pool": "Split-and-claim, 10,000, bigger pool",
        "a20000": "Split-and-claim, 20,000",
        "a40000": "Split-and-claim, 40,000",
        "a100000": "Split-and-claim, 100,000",
        "a10000": "Split-and-claim, 10,000, default pool",
        "b100": "Recycling, 100",
        "b1000": "Recycling, 1,000",
        "b_paced": "Recycling, 10,000 in waves",
        "b_pool": "Recycling, 10,000, bigger pool",
        "b20000": "Recycling, 20,000",
        "b40000": "Recycling, 40,000",
        "b10000": "Recycling, 10,000, default pool",
        "b100000": "Recycling, 100,000",
    }
    status = {
        "workload-pass": "pass",
        "incomplete": "incomplete",
        "launch-timing-failure": "fail: launch too slow",
    }
    fig, ax = plt.subplots(figsize=(8.6, 7.0))
    for i, case in enumerate(order):
        v = lifecycle(case)["verifiedOutcome"]
        per_actor = 2 if case.startswith("a") else 1
        requested = v["requestedActors"] * per_actor
        pct = 100 * v["receiptVerified"] / requested
        ok = v["outcome"] == "workload-pass"
        ax.barh(i, pct, height=0.7, color=BLUE if ok else GREY, hatch=None if ok else "////", edgecolor=SURFACE, linewidth=0)
        text = f"{pct:.0f}%  {v['receiptVerified']:,} of {requested:,}  ·  {status[v['outcome']]}"
        if v["ciShutdownFailure"]:
            text += " (CI shutdown failed later)"
        label_bar(ax, i, pct, text, 160)
    ax.set_yticks(range(len(order)), [names[c] for c in order])
    style_hbar(ax, 160)
    ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.axhline(7.5, color=AXIS, linewidth=1)
    ax.set_xlabel("Verified receipts as a share of requested extrinsics")
    ax.set_title("Lifecycle cases: how many extrinsics have a verified receipt?")
    save(fig, "lifecycle-completion.svg")


if __name__ == "__main__":
    topup_timing()
    recycling_timing()
    claim_finality()
    pool()
    blocks()
    split_claim_timing()
    completion()
