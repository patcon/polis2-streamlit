import streamlit as st
import streamlit.components.v1 as components
import valency_anndata as val
import datamapplot
import numpy as np

st.set_page_config(
    page_title="Pol.is → Polis2 Statements",
    layout="wide",
)

st.title("Pol.is Report → Polis2 Statements Explorer")

st.markdown(
    """
    Paste a **Pol.is report URL** (e.g. `https://pol.is/report/xxxx`)
    This app will load the report, run the Polis2 statements recipe,
    and render an interactive datamapplot.
    """
)

# ----------------------------
# Inputs (pre-filled from ?report=...&lang=... query params)
# ----------------------------
params = st.query_params

report_url = st.text_input(
    "Pol.is report URL",
    value=params.get("report", "https://pol.is/report/r4zdxrdscmukmkakmbz3k"),
)

translate_to = st.text_input(
    "Translate to language (2-letter code, e.g. `en`, `fr`). Leave blank to skip.",
    value=params.get("lang", ""),
    max_chars=2,
)

run = st.button("Run analysis")

# ----------------------------
# Cached loader
# ----------------------------
@st.cache_data(show_spinner=True)
def load_polis_report(url: str, translate_to: str | None = None):
    kwargs = {}
    if translate_to:
        kwargs["translate_to"] = translate_to
    return val.datasets.polis.load(url, **kwargs)

# ----------------------------
# Main logic
# ----------------------------
if run:
    if not report_url.strip():
        st.error("Please enter a Pol.is report URL.")
        st.stop()

    with st.spinner("Loading Pol.is report…"):
        adata = load_polis_report(report_url, translate_to=translate_to.strip() or None)

    st.success(f"Loaded report with {adata.shape[1]} statements")

    with st.spinner("Running recipe_polis2_statements…"):
        val.tools.recipe_polis2_statements(adata)

    # ----------------------------
    # Interactive datamapplot
    # ----------------------------
    st.subheader("Statement Map")

    label_layers = adata.varm["evoc_polis2"].transpose()
    label_layers_humanized = [
        [f"Zoom{zoom_level}:Group{group_id}" for group_id in row]
        for zoom_level, row in enumerate(reversed(label_layers), start=1)
    ]

    fig = datamapplot.create_interactive_plot(
        adata.varm["content_umap"],
        *label_layers_humanized,
        title=f"Polis Report",
        sub_title=f"{adata.shape[1]} statements",
        hover_text=adata.var["content"],
        enable_search=True,
        darkmode=True,
        height=600,
        palette_theta_range=np.pi / 8,
        point_radius_min_pixels=8,
    )

    components.html(fig._html_str, height=620, scrolling=True)

    # ----------------------------
    # Optional: show raw tables
    # ----------------------------
    with st.expander("Inspect derived variables"):
        st.write("`adata.var`")
        st.dataframe(adata.var.head(50))

        st.write("`adata.varm['evoc_polis2']`")
        st.write(adata.varm["evoc_polis2"])
