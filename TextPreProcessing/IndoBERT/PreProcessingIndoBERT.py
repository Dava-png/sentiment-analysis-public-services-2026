import os
import re
import pandas as pd

print("STEP BY STEP: TEXT PREPROCESSING KHUSUS INDOBERT")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Memuat dataset master
df = pd.read_csv(
    os.path.join(
        BASE_DIR, "../../DatasetFullAnotasi/dataset_master_full_anotation.csv"
    )
)
print(f"-> Berhasil memuat data master: {len(df):,} baris")

# 2. Kamus Slang / Bahasa Gaul (Sama seperti sebelumnya)
slang_dict = {
    "gak": "tidak",
    "ga": "tidak",
    "nggak": "tidak",
    "gk": "tidak",
    "tdk": "tidak",
    "yg": "yang",
    "utk": "untuk",
    "bgt": "banget",
    "dgn": "dengan",
    "dr": "dari",
    "tp": "tapi",
    "sdh": "sudah",
    "udh": "sudah",
    "blm": "belum",
    "bs": "bisa",
    "jgn": "jangan",
    "jg": "juga",
    "kalo": "kalau",
    "krn": "karena",
    "sm": "sama",
    "sy": "saya",
    "org": "orang",
    "bkn": "bukan",
    "byk": "banyak",
    "dlm": "dalam",
    "dpt": "dapat",
    "hrs": "harus",
    "lg": "lagi",
    "msh": "masih",
    "pake": "pakai",
    "aja": "saja",
    "apk": "aplikasi",
    "app": "aplikasi",
    "eror": "error",
    "mntap": "mantap",
    "oke": "oke",
    "makasih": "terima kasih",
    "tlg": "tolong",
    "susah": "sulit",
    "ribet": "rumit",
    "gimana": "bagaimana",
    "knp": "kenapa",
    "bikin": "membuat",
    "donlod": "unduh",
    "login": "masuk",
    "logout": "keluar",
}


def preprocess_indobert(text):
  if pd.isna(text):
    return ""
  # Lowercase (Case Folding)
  text = str(text).lower()

  # Hapus URL, mention, hashtag berlebih
  text = re.sub(r"http\S+|www\.\S+", " ", text)
  text = re.sub(r"@[A-Za-z0-9_]+|#[A-Za-z0-9_]+", " ", text)

  # PERBEDAAN UTAMA DARI SVM:
  # Pertahankan tanda baca dasar (? ! . ,) dan huruf/angka agar konteks kalimat utuh
  text = re.sub(r"[^a-z0-9\s\?\!\.,]", " ", text)

  # Normalisasi slang
  words = text.split()
  norm_words = [slang_dict.get(w, w) for w in words]

  # Tanpa Stopword Removal (struktur kalimat utuh untuk Transformer)
  return re.sub(r"\s+", " ", " ".join(norm_words)).strip()


# 3. Jalankan preprocessing ke kolom teks
print("-> Sedang membersihkan teks untuk jalur IndoBERT...")
df["text_clean_indobert"] = df["review_text"].apply(preprocess_indobert)

# 4. Simpan hasil preprocessing IndoBERT ke file CSV terpisah
output_file = "dataset_preprocessed_indobert_2026.csv"
df[
    [
        "app_name",
        "review_id",
        "score",
        "review_text",
        "text_clean_indobert",
        "Kategori",
    ]
].to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"\n[SUKSES] Preprocessing IndoBERT selesai!")
print(f"-> File disimpan sebagai: {output_file}")

# Tampilkan 5 contoh perbandingan teks asli vs teks bersih IndoBERT
print("\nContoh Hasil Preprocessing IndoBERT:")
for i in range(5):
  print(f"Asli   : {df.loc[i, 'review_text']}")
  print(f"IndoBERT: {df.loc[i, 'text_clean_indobert']}")
  print("-" * 40)