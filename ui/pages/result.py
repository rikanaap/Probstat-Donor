import pandas as pd
import streamlit as st
from calc import config
from logic import data_io, insights, report, scenario, synthetic
from .. import components as c


def _analyze(up):
    """Dijalankan hanya saat tombol Analisis ditekan, dengan indikator proses."""
    with st.status("Memproses data...", expanded=True) as status:
        try:
            st.write("Membaca file...")
            raw = data_io.read_table(up)
            st.write("Memeriksa isi file...")
            errs = data_io.validate(raw)
        except Exception:
            status.update(label="File tidak bisa dibaca", state="error")
            st.error("File tidak bisa dibaca. Pastikan formatnya Excel atau CSV yang benar.")
            return
        if errs:
            status.update(label="Isi file belum sesuai", state="error")
            st.error("\n\n".join(errs))
            return
        st.write("Menghitung hasil...")
        df = data_io.clean(raw)
        st.session_state["report"] = report.build(df)
        st.session_state["data"] = df
        st.session_state.pop("sim", None)
        status.update(label="Selesai", state="complete", expanded=False)


def _upload():
    with st.expander("Data survei", expanded="report" not in st.session_state):
        up = st.file_uploader("Unggah hasil survei (Excel atau CSV)", type=["xlsx", "xls", "csv"])
        l, r = st.columns(2)
        run = l.button("Analisis data", type="primary", disabled=up is None, use_container_width=True)
        r.download_button("Unduh contoh data (Excel)", synthetic.sample_xlsx(), "contoh_data_sintetis.xlsx",
                          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                          use_container_width=True, help="Data buatan untuk mencoba aplikasi.")
        if up is None:
            st.caption("Pilih file dulu, lalu tekan Analisis data.")
        if run:
            _analyze(up)


def _simulation(df, top):
    st.markdown("##### Coba bayangkan: kalau diperbaiki?")
    with st.container(border=True):
        with st.form("sim_form"):
            choice = st.multiselect("Layanan yang diperbaiki", list(config.ITEMS), format_func=config.ITEMS.get,
                                    default=[p["key"] for p in top])
            a, b = st.columns(2)
            step = a.slider("Naik berapa nilai?", 0.5, 2.0, 1.0, 0.5)
            total = b.number_input("Jumlah orang yang hadir", 1, 100000, 300)
            go = st.form_submit_button("Hitung perkiraan", type="primary")
        if go:
            if not choice:
                st.warning("Pilih minimal satu layanan.")
            else:
                with st.spinner("Menghitung perkiraan..."):
                    st.session_state["sim"] = scenario.what_if(df, choice, step, int(total))
        r = st.session_state.get("sim")
        if r is None:
            st.info("Atur pilihan di atas, lalu tekan **Hitung perkiraan**.")
            return
        low_diff = int(round(r["ci_diff"][0]))
        high_diff = int(round(r["ci_diff"][1]))
        st.success(f"Perkiraan: bertambah sekitar **+{r['donor_tambahan']:.0f} donor berniat kembali** per periode "
                   f"(rentang keyakinan 95%: **{low_diff} – {high_diff} donor**).")
        m1, m2 = st.columns(2)
        m1.metric("Donor Berniat Kembali (Saat Ini)", f"{r['exp0']:.0f} orang", f"Peluang: {r['p0']:.1%}")
        m2.metric("Setelah Perbaikan", f"{r['exp1']:.0f} orang", f"+{r['donor_tambahan']:.0f} orang ({r['p1']:.1%})")
        c.info("Landasan Statistik",
               "Perhitungan ini murni berbasis teori probabilitas & statistika:\n\n"
               "- **Regresi Linear (OLS)** untuk menghitung pengaruh perbaikan layanan.\n"
               "- **Distribusi Normal Residual** $\\mathcal{N}(0, \\sigma^2)$ untuk menghitung peluang berniat kembali ($Y \\ge 4$).\n"
               "- **Distribusi Binomial** $\\text{Binomial}(N, p)$ untuk menghitung nilai harapan jumlah donor riil dan Interval Keyakinan 95%.")


def render():
    st.subheader("Apa yang perlu diperbaiki?")
    _upload()
    rep, df = st.session_state.get("report"), st.session_state.get("data")
    if rep is None:
        c.empty_state("Belum ada hasil", "Unggah hasil survei lalu tekan **Analisis data**. Belum punya? Unduh contoh data di panel Data survei.")
        return

    top, (q_level, q_text) = rep["top"], rep["quality"]
    with st.container(border=True):
        st.markdown(f"<div class='hero'>Fokus utama: <b>{top[0]['item']}</b><br>"
                    f"<span class='small'>Nilai rata-rata {top[0]['skor']} dari 5, dan paling berpengaruh pada keinginan donor kembali.</span></div>",
                    unsafe_allow_html=True)
        l, r = st.columns([5, 1])
        l.caption(f"Kualitas data: **{q_level}**. {q_text}")
        with r:
            c.info("Arti?", "Menunjukkan apakah jawaban sudah cukup banyak dan konsisten untuk dipercaya. Kalau **Kurang**, kumpulkan lebih banyak form dulu.")

    st.markdown("##### Tiga hal yang perlu diperbaiki")
    for col, p in zip(st.columns(len(top)), top):
        text, color = insights.level(p["skor"])
        with col.container(border=True):
            st.markdown(f"**{p['item']}**")
            st.metric("Nilai", f"{p['skor']} / 5", label_visibility="collapsed")
            st.markdown(f":{color}[{text}]")

    with st.expander("Lihat nilai semua layanan"):
        c.score_chart(rep["scores"], insights.level)
    with st.expander("Bandingkan antar sesi"):
        s = rep["sessions"]
        st.write(f"Sesi **{s['rendah']}** paling kurang memuaskan, **{s['tinggi']}** paling baik." if s["nyata"]
                 else "Kepuasan antar sesi relatif sama.")
        st.dataframe(pd.Series(s["skor"], name="Kepuasan (1-5)"), use_container_width=True)

    _simulation(df, top)
