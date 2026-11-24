import pandas as pd
import streamlit as st
from calc import config
from logic import data_io, plan, synthetic
from .. import components as c


def render():
    st.subheader("Berapa form yang perlu dibagikan?")
    st.caption("Isi satu hal saja, hasilnya langsung muncul di bawah.")
    with st.container(border=True):
        mode = st.radio("Anda punya data apa?", ["Hanya perkiraan jumlah donor", "Catatan jam kedatangan donor"], horizontal=True)
        if mode.startswith("Hanya"):
            cols = st.columns(len(config.DEFAULT_SESSIONS))
            counts = {s: col.number_input(f"Donor sesi {s}", 0, 100000, 300) for s, col in zip(config.DEFAULT_SESSIONS, cols)}
            st.caption("Perkiraan jumlah donor selama seluruh survei")
        else:
            up = st.file_uploader("File Excel atau CSV dengan kolom 'timestamp'", type=["xlsx", "xls", "csv"])
            st.download_button("Unduh contoh catatan kedatangan (Excel)", synthetic.sample_arrivals_xlsx(),
                               "contoh_jam_kedatangan_donor.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               help="Data buatan untuk mencoba. Ganti isinya dengan catatan Anda, kolom 'timestamp' berisi tanggal dan jam datang.")
            if up:
                with st.spinner("Membaca file..."):
                    table = data_io.read_table(up)
                if "timestamp" not in table.columns:
                    st.error("Kolom 'timestamp' tidak ditemukan di file.")
                    return
                times = table["timestamp"]
            elif st.toggle("Pakai contoh catatan (demo)"):
                times = synthetic.generate_arrivals()
            else:
                return
            with st.spinner("Mengelompokkan per sesi..."):
                counts = plan.counts_from_times(times, config.DEFAULT_SESSIONS)
        l, r = st.columns([4, 1])
        level = l.select_slider("Seberapa teliti?", list(plan.PRECISION), value="Standar (disarankan)")
        with r:
            c.info("Apa ini?", "Makin teliti, makin banyak form yang harus dibagikan. **Standar** cukup untuk sebagian besar kebutuhan.")

    rows = plan.make_plan(counts, level)
    total = sum(x["Form yang dibagikan"] for x in rows)
    with st.container(border=True):
        st.markdown(f"<div class='hero'>Total form yang perlu dibagikan: <b>{total}</b></div>", unsafe_allow_html=True)
        cols = st.columns(len(rows))
        for col, x in zip(cols, rows):
            col.metric(f"Sesi {x['Sesi']}", f"{x['Form yang dibagikan']} form")
            col.caption(f"Beri form ke 1 dari setiap {x['Beri form ke setiap donor ke-']} donor")
        c.info("Kenapa tidak semua donor?", "Cukup sebagian donor yang dipilih secara bergiliran. Hasilnya tetap bisa mewakili semua donor, dan petugas tidak kewalahan.")
    for w in plan.warnings(rows):
        st.warning(w)