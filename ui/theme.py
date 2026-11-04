"""Gaya tambahan. Warna utama diatur di .streamlit/config.toml."""
import streamlit as st

CSS = """
<style>
.block-container { max-width: 860px; padding-top: 1.5rem; }
h1 { font-size: 1.9rem !important; }
div[data-testid="stMetricValue"] { font-size: 1.6rem; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 12px; }
.hero { font-size: 1.35rem; line-height: 1.5; }
.small { color: #6B7280; font-size: .9rem; }
</style>
"""


def apply():
    st.markdown(CSS, unsafe_allow_html=True)
