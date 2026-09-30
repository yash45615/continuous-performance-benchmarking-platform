import argparse
import json
from pathlib import Path


def percentage_change(
    baseline,
    current
):

    if baseline == 0:

        return 0.0

    return (
        (current - baseline)
        / baseline
    ) * 100


def compare(
    baseline,
    current,
    latency_threshold=10.0
):

    latency_change = percentage_change(
        baseline["p95_ms"],
        current["p95_ms"]
    )

    failure_change = (
        current.get("failures", 0)
        - baseline.get("failures", 0)
    )

    reasons = []

    if latency_change > latency_threshold:

        reasons.append(
            (
                "P95 latency increased by "
                f"{latency_change:.2f}%"
            )
        )

    if failure_change > 0:

        reasons.append(
            (
                "Failures increased by "
                f"{failure_change}"
            )
        )

    regression = len(reasons) > 0

    return {
        "regression": regression,

        "latency_change_pct": round(
            latency_change,
            2
        ),

        "failure_change": failure_change,

        "reasons": reasons
    }


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--baseline",
        required=True
    )

    parser.add_argument(
        "--current",
        required=True
    )

    parser.add_argument(
        "--latency-threshold",
        type=float,
        default=10.0
    )

    parser.add_argument(
        "--out",
        default="data/comparison.json"
    )

    args = parser.parse_args()

    baseline = json.loads(
        Path(
            args.baseline
        ).read_text(
            encoding="utf-8"
        )
    )

    current = json.loads(
        Path(
            args.current
        ).read_text(
            encoding="utf-8"
        )
    )

    result = compare(
        baseline,
        current,
        args.latency_threshold
    )

    output = Path(args.out)

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    if result["regression"]:

        print(
            "\nPERFORMANCE REGRESSION DETECTED"
        )

        raise SystemExit(1)

    print(
        "\nPERFORMANCE CHECK PASSED"
    )


if __name__ == "__main__":
    main()