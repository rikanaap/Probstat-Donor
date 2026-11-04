"""Komponen tampilan yang dipakai ulang."""
import plotly.graph_objects as go
import streamlit as st

TONE_HEX = {"green": "#16A34A", "orange": "#D97706", "red": "#DC2626"}


def info(label: str, text: str):
    """Panel penjelasan kecil untuk istilah yang membingungkan."""
    with st.popover(f"ℹ️ {label}"):
        st.markdown(text)


def empty_state(title: str, text: str):
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.write(text)


def score_chart(scores, level_fn):
    s = scores.sort_values(ascending=False)
    colors = [TONE_HEX[level_fn(v)[1]] for v in s]
    fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=colors,
                           text=[f"{v:.1f}" for v in s.values], textposition="outside"))
    fig.update_layout(height=60 + 42 * len(s), margin=dict(l=0, r=30, t=10, b=0), xaxis=dict(range=[1, 5.4], title="Nilai (1-5)"),
                      yaxis=dict(autorange="reversed"), plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
