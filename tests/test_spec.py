import pandas as pd
import pytest

from imfcharts import Chart


def _sample_data():
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=3, freq="MS"),
            "GDP": [1.0, 2.0, 3.0],
            "Inflation": [4.0, 5.0, 6.0],
        }
    )


def test_from_spec_builds_chart_without_mutating_input_data():
    df = _sample_data()
    original_columns = list(df.columns)
    spec = {
        "data": {"indexcol": "date"},
        "marks": [
            {
                "type": "line",
                "cols": "GDP",
                "style": {"color": "#004C97", "linewidth": 2},
            },
            {
                "type": "bar",
                "cols": "Inflation",
                "axis": "right",
                "style": {"color": "#B1B3B3"},
            },
        ],
        "text": {
            "title": "Output and Prices",
            "subtitle": "(Index)",
            "ytitle": "GDP",
        },
        "axes": {
            "x": {"range": "2024-01:", "format": "M"},
            "y": {"range": [0, 4]},
            "right_y": {"range": [0, 8]},
        },
        "legend": {"left": 0.35, "bottom": 0.82, "ncol": 2},
        "layout": {"width": 7, "height": 4},
        "annotations": {"hlines": [{"y": 2, "color": "black"}]},
    }

    chart = Chart.from_spec(spec, data=df)

    assert chart.to_spec() == spec
    assert chart.titletext == "Output and Prices"
    assert chart.legend_labels == ["GDP", "Inflation"]
    assert list(df.columns) == original_columns
    assert "date" in df.columns


def test_validate_spec_rejects_unknown_line_style_keys():
    spec = {
        "marks": [
            {
                "type": "line",
                "cols": "GDP",
                "style": {"not_a_line_option": True},
            }
        ]
    }

    with pytest.raises(ValueError, match="Unknown line style keys"):
        Chart.validate_spec(spec)


def test_validate_spec_rejects_unknown_sections():
    with pytest.raises(ValueError, match="Unknown spec sections"):
        Chart.validate_spec({"series": []})
