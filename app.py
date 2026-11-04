import streamlit as st
from ui import theme
from ui.pages import plan, result

st.set_page_config(page_title="Donor Kembali", page_icon="🩸", layout="centered")
theme.apply()
st.title("🩸 Donor Kembali")
st.caption("Cari tahu apa yang membuat donor mau datang lagi.")
PAGES = {"1. Rencana form": plan.render, "2. Hasil & perkiraan": result.render}
choice = st.segmented_control("Langkah", list(PAGES), default=list(PAGES)[0], label_visibility="collapsed")
PAGES[choice or list(PAGES)[0]]()
