import json
from pathlib import Path


RESULTS_FILE = Path("results/evaluation.json")
REPORT_FILE = Path("results/benchmark_report.md")


def pct(value):
    return f"{value * 100:.1f}%"


def main():
    with open(RESULTS_FILE, encoding="utf-8") as file:
        report = json.load(file)

    evaluation = report["evaluation"]
    baseline = report["baseline"]
    jev = report["jev"]

    lines = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    lines.append("# JEV Support Decision Benchmark")
    lines.append("")

    # -------------------------------------------------
    # EXPERIMENTAL SETUP
    # -------------------------------------------------

    lines.append("## Experimental setup")
    lines.append("")
    lines.append(
        "This benchmark compares the JEV-backed decision provider "
        "against the deterministic rule-based baseline using the "
        "same datasets and evaluation pipeline."
    )
    lines.append("")

    lines.append(
        f"- Escalation threshold: "
        f"`{evaluation['escalation_threshold']}`"
    )

    lines.append("- Datasets:")

    for name, path in evaluation["datasets"].items():
        sample_count = len(baseline[name]["results"])

        lines.append(
            f"  - {name}: `{path}` "
            f"({sample_count} examples)"
        )

    lines.append("")

    # -------------------------------------------------
    # RESULTS
    # -------------------------------------------------

    lines.append("## Results")
    lines.append("")

    lines.append(
        "| Dataset | N | Provider | Category Accuracy | "
        "Escalation Accuracy | Urgency MAE |"
    )

    lines.append(
        "|---|---:|---|---:|---:|---:|"
    )

    for dataset in evaluation["datasets"]:
        baseline_metrics = baseline[dataset]["metrics"]
        jev_metrics = jev[dataset]["metrics"]

        baseline_n = len(baseline[dataset]["results"])
        jev_n = len(jev[dataset]["results"])

        lines.append(
            f"| {dataset} | {baseline_n} | "
            f"Rule-based baseline | "
            f"{pct(baseline_metrics['category_accuracy'])} | "
            f"{pct(baseline_metrics['escalation_accuracy'])} | "
            f"{baseline_metrics['urgency_mae']:.3f} |"
        )

        lines.append(
            f"| {dataset} | {jev_n} | "
            f"JEV | "
            f"{pct(jev_metrics['category_accuracy'])} | "
            f"{pct(jev_metrics['escalation_accuracy'])} | "
            f"{jev_metrics['urgency_mae']:.3f} |"
        )

    lines.append("")

    # -------------------------------------------------
    # COMPARISON
    # -------------------------------------------------

    lines.append("## JEV vs baseline")
    lines.append("")

    for dataset in evaluation["datasets"]:
        b = baseline[dataset]["metrics"]
        j = jev[dataset]["metrics"]

        category_delta = (
            j["category_accuracy"]
            - b["category_accuracy"]
        )

        escalation_delta = (
            j["escalation_accuracy"]
            - b["escalation_accuracy"]
        )

        urgency_delta = (
            b["urgency_mae"]
            - j["urgency_mae"]
        )

        lines.append(f"### {dataset.capitalize()}")
        lines.append("")

        lines.append(
            f"- Category accuracy change: "
            f"{category_delta * 100:+.1f} percentage points"
        )

        lines.append(
            f"- Escalation accuracy change: "
            f"{escalation_delta * 100:+.1f} percentage points"
        )

        lines.append(
            f"- Urgency MAE reduction: "
            f"{urgency_delta:.3f}"
        )

        lines.append("")

    # -------------------------------------------------
    # INTERPRETATION
    # -------------------------------------------------

    lines.append("## Interpretation")
    lines.append("")

    lines.append(
        "On this benchmark, JEV produced higher category accuracy "
        "and lower urgency error than the rule-based baseline across "
        "the development, validation, and test datasets."
    )

    lines.append("")

    lines.append(
        "Escalation accuracy also exceeded the baseline on the "
        "validation and test datasets, while matching the baseline "
        "on the development dataset."
    )

    lines.append("")

    lines.append(
        "These results demonstrate performance on the supplied "
        "benchmark datasets. They should not be interpreted as proof "
        "of production-level reliability or generalization to unseen "
        "real-world support traffic."
    )

    lines.append("")

    # -------------------------------------------------
    # REPRODUCIBILITY
    # -------------------------------------------------

    lines.append("## Reproducibility")
    lines.append("")

    lines.append(
        "The raw per-example predictions, confusion matrices, "
        "classification errors, and urgency errors are retained in "
        "`results/evaluation.json`."
    )

    lines.append("")

    lines.append(
        "The benchmark uses separate development, validation, and "
        "test datasets. This report records the resulting performance "
        "on each split but does not independently verify whether the "
        "test set was excluded from all prior prompt or threshold "
        "decisions."
    )

    lines.append("")

    # -------------------------------------------------
    # WRITE REPORT
    # -------------------------------------------------

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(
        f"Benchmark report written to: {REPORT_FILE}"
    )


if __name__ == "__main__":
    main()