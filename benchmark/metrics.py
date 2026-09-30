from statistics import mean, median, quantiles


def percentile(values, percentile_value):

    if not values:
        return 0.0

    if len(values) == 1:
        return float(values[0])

    sorted_values = sorted(values)

    index = (
        (len(sorted_values) - 1)
        * percentile_value
        / 100
    )

    lower = int(index)

    upper = min(
        lower + 1,
        len(sorted_values) - 1
    )

    fraction = index - lower

    return (
        sorted_values[lower]
        + (
            sorted_values[upper]
            - sorted_values[lower]
        )
        * fraction
    )


def summarize(samples):

    values = [
        float(value)
        for value in samples
    ]

    if not values:

        return {
            "count": 0,
            "avg_ms": 0,
            "p50_ms": 0,
            "p95_ms": 0,
            "p99_ms": 0,
            "min_ms": 0,
            "max_ms": 0
        }

    return {
        "count": len(values),

        "avg_ms": round(
            mean(values),
            2
        ),

        "p50_ms": round(
            percentile(values, 50),
            2
        ),

        "p95_ms": round(
            percentile(values, 95),
            2
        ),

        "p99_ms": round(
            percentile(values, 99),
            2
        ),

        "min_ms": round(
            min(values),
            2
        ),

        "max_ms": round(
            max(values),
            2
        )
    }