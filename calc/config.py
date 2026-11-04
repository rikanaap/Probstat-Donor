"""Konstanta aplikasi. Ubah di sini, bukan di tempat lain."""
ITEMS = {
    "alur": "Kejelasan alur",
    "daftar": "Kecepatan pendaftaran",
    "tunggu": "Lama menunggu",
    "ramah": "Keramahan petugas",
    "tusuk": "Kenyamanan penusukan",
    "ruang": "Kenyamanan ruang istirahat",
    "makanan": "Kualitas makanan/minuman",
}
SATISFACTION = "kepuasan"
OUTCOME = "niat_kembali"
SESSION_COL = "sesi"
DEFAULT_SESSIONS = {"Pagi": (6, 11), "Siang": (11, 15), "Sore": (15, 20)}  # jam mulai, jam selesai
REQUIRED_COLS = [SESSION_COL, *ITEMS, SATISFACTION, OUTCOME]
