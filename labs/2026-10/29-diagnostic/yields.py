def average_yield(yields: dict[str, float | None]) -> float:
    """Average yield across runs that were measured.

    None means the run wasn't measured and is excluded.
    0.0 is a real measurement and is included.
    If no runs were measured, raise ValueError.
    """
    measured = [v for v in yields.values() if v is not None]
    if not measured:
        raise ValueError("no measured runs to average")
    return sum(measured) / len(measured)
