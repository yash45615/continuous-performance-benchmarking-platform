import argparse
import json
import time
from pathlib import Path

import httpx

from benchmark.metrics import summarize


def run_benchmark(
    base_url,
    path,
    request_count
):

    latencies = []

    failures = 0

    with httpx.Client(
        base_url=base_url,
        timeout=10.0
    ) as client:

        for _ in range(request_count):

            start = time.perf_counter()

            try:

                response = client.get(path)

                elapsed = (
                    time.perf_counter()
                    - start
                ) * 1000

                latencies.append(elapsed)

                if response.status_code >= 400:
                    failures += 1

            except Exception:

                failures += 1

    metrics = summarize(latencies)

    metrics.update(
        {
            "url": base_url,
            "path": path,
            "failures": failures,
            "success_rate": round(
                (
                    (
                        request_count
                        - failures
                    )
                    / request_count
                ) * 100,
                2
            )
        }
    )

    return metrics


def main():

    parser = argparse.ArgumentParser(
        description="Run HTTP performance benchmark"
    )

    parser.add_argument(
        "--url",
        required=True
    )

    parser.add_argument(
        "--path",
        required=True
    )

    parser.add_argument(
        "--requests",
        type=int,
        default=100
    )

    parser.add_argument(
        "--out",
        default="data/latest.json"
    )

    args = parser.parse_args()

    result = run_benchmark(
        args.url,
        args.path,
        args.requests
    )

    output_path = Path(args.out)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
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


if __name__ == "__main__":
    main()