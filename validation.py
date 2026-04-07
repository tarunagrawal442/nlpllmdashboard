def validate_chart_spec(spec, df):
    allowed_chart_types = {"bar", "line", "scatter", "histogram", "box", "pie"}
    allowed_aggs = {"sum", "mean", "count", "min", "max", None}

    if spec["chart_type"] not in allowed_chart_types:
        raise ValueError("Invalid chart type")

    for field in ["x", "y", "color"]:
        if spec[field] is not None and spec[field] not in df.columns:
            raise ValueError(f"Invalid column in {field}: {spec[field]}")

    if spec["aggregation"] not in allowed_aggs:
        raise ValueError("Invalid aggregation")

    for f in spec["filters"]:
        if f["column"] not in df.columns:
            raise ValueError(f"Invalid filter column: {f['column']}")
