import streamlit as st
import valency_anndata as val

st.set_page_config(
    page_title="Pol.is → Polis2 Statements",
    layout="wide",
)

st.title("Pol.is Report → Polis2 Statements Explorer")

st.markdown(
    """
    Paste a **Pol.is report URL** (e.g. `https://pol.is/report/xxxx`)  
    This app will:
    - Load the report
    - Run the Polis2 statements recipe
    - Show embeddings and diagnostics
    """
)

# ----------------------------
# Inputs
# ----------------------------
report_url = st.text_input(
    "Pol.is report URL",
    value="https://pol.is/report/r7wehfsmutrwndviddnii",
)

run = st.button("Run analysis")

# ----------------------------
# Cached loader
# ----------------------------
@st.cache_data(show_spinner=True)
def load_polis_report(url: str):
    return val.datasets.polis.load(url)

# ----------------------------
# Main logic
# ----------------------------
if run:
    if not report_url.strip():
        st.error("Please enter a Pol.is report URL.")
        st.stop()

    with st.spinner("Loading Pol.is report…"):
        adata = load_polis_report(report_url)

    st.success(f"Loaded report with {adata.shape[1]} statements")

    # ----------------------------
    # Run recipe
    # ----------------------------
    st.subheader("Polis2 Statements Recipe")

    with st.spinner("Running recipe_polis2_statements…"):
        with val.viz.schematic_diagram(diff_from=adata):
            val.tools.recipe_polis2_statements(adata)

    st.caption("Schematic diagram shows transformations applied to the AnnData object.")

    # ----------------------------
    # Embedding plot
    # ----------------------------
    st.subheader("Statement Embedding")

    fig = val.viz.embedding(
        adata.transpose(),
        basis="content_umap",
        color=["evoc_polis2_top", "moderation_state"],
        return_fig=True,  # important for Streamlit
    )

    st.pyplot(fig, use_container_width=True)

    # ----------------------------
    # Datamapplot (placeholder)
    # ----------------------------
    st.subheader("Cluster Overview (Datamapplot)")

    st.info(
        "Interactive datamapplot rendering is not yet Streamlit-native. "
        "Showing a placeholder image for now."
    )

    st.image(
        "https://i.imgur.com/CMiO6nu.png",
        caption="Example datamapplot output",
        use_container_width=True,
    )

    # ----------------------------
    # Optional: show raw tables
    # ----------------------------
    with st.expander("Inspect derived variables"):
        st.write("`adata.var`")
        st.dataframe(adata.var.head(50))

        st.write("`adata.varm['evoc_polis2']`")
        st.write(adata.varm["evoc_polis2"])
