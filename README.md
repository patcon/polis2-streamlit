# Streamlit-Polis2

A Streamlit app that loads a [Pol.is](https://pol.is) report, runs the Polis2 statements recipe, and renders an interactive [datamapplot](https://github.com/TutteInstitute/datamapplot).

## Usage

```sh
uv run streamlit run streamlit_app.py
```

### Query parameters

Pre-fill inputs via URL:

| Param    | Description                        | Example          |
|----------|------------------------------------|------------------|
| `report` | Pol.is report URL                  | `https://pol.is/report/r4zdxrdscmukmkakmbz3k` |
| `lang`   | 2-letter language code to translate to | `en`         |

Example: `https://your-app.streamlit.app/?report=https://pol.is/report/r4zdxrdscmukmkakmbz3k&lang=en`
