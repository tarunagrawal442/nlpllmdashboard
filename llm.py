import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chart_spec(df, user_prompt):
    schema_info = {
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "sample_rows": df.head(5).to_dict(orient="records"),
        "row_count": len(df),
    }

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "developer",
                "content": (
                    "You are a data visualization planner. "
                    "Return only a JSON object that matches the requested schema. "
                    "Use only the columns provided. "
                    "Prefer line charts for time series, bar charts for grouped comparisons, "
                    "scatter for relationship analysis, histogram for distributions, "
                    "and box plots for spread/outliers."
                ),
            },
            {
                "role": "user",
                "content": json.dumps({
                    "task": "Create a chart specification from the dataset metadata and user request.",
                    "dataset": schema_info,
                    "user_prompt": user_prompt
                })
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "chart_spec",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "enum": ["bar", "line", "scatter", "histogram", "box", "pie"]
                        },
                        "x": {"type": ["string", "null"]},
                        "y": {"type": ["string", "null"]},
                        "color": {"type": ["string", "null"]},
                        "aggregation": {
                            "type": ["string", "null"],
                            "enum": ["sum", "mean", "count", "min", "max", None]
                        },
                        "filters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "column": {"type": "string"},
                                    "op": {
                                        "type": "string",
                                        "enum": ["=", "!=", ">", "<", ">=", "<="]
                                    },
                                    "value": {}
                                },
                                "required": ["column", "op", "value"]
                            }
                        },
                        "title": {"type": "string"}
                    },
                    "required": ["chart_type", "x", "y", "color", "aggregation", "filters", "title"]
                },
                "strict": True
            }
        }
    )

    content = response.choices[0].message.content
    return json.loads(content)
