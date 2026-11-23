import re
import pandas as pd
import os

print("=== STEP BY STEP: TEXT PREPROCESSING KHUSUS SVM ===")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Memuat dataset master
df = pd.read_csv(os.path.join(BASE_DIR, "../../DatasetFullAnotasi/dataset_master_full_anotation.csv"))
print(f"-> Berhasil memuat data master: {len(df):,} baris")
    
# 2. Kamus Slang / Bahasa Gaul
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

# Stopwords umum dengan proteksi kata negasi penting
stopwords_id = {
    "yang",
    "di",
    "ke",
    "dari",
    "dan",
    "atau",
    "ini",
    "itu",
    "untuk",
    "pada",
    "oleh",
    "adalah",
    "sebagai",
    "bahwa",
    "dengan",
}
keep_words = {
    "tidak",
    "bukan",
    "belum",
    "jangan",
    "kurang",
    "tanpa",
    "gagal",
    "sulit",
    "lama",
    "bagus",
    "baik",
    "membantu",
    "mudah",
    "cepat",
    "mantap",
    "kecewa",
    "parah",
    "buruk",
}
stopwords_svm = stopwords_id - keep_words


def preprocess_svm(text):
  if pd.isna(text):
    return ""
  # Lowercase
  text = str(text).lower()
  # Hapus URL & mention
  text = re.sub(r"http\S+|www\.\S+", " ", text)
  text = re.sub(r"@[A-Za-z0-9_]+|#[A-Za-z0-9_]+", " ", text)
  # Hapus angka & tanda baca (hanya sisakan huruf)
  text = re.sub(r"[^a-z\s]", " ", text)

  # Normalisasi slang
  words = text.split()
  norm_words = [slang_dict.get(w, w) for w in words]

  # Stopword removal (buang kata umum, pertahankan kata penting & negasi)
  tokens = [w for w in norm_words if w not in stopwords_svm and len(w) > 1]
  return " ".join(tokens)


# 3. Jalankan preprocessing ke kolom teks
print("-> Sedang membersihkan teks untuk jalur SVM...")
df["text_clean_svm"] = df["review_text"].apply(preprocess_svm)

# 4. Simpan hasil preprocessing SVM ke file CSV terpisah
output_file = "dataset_preprocessed_svm_2026.csv"
df[["app_name", "review_id", "score", "review_text", "text_clean_svm", "Kategori"]].to_csv(
    output_file, index=False, encoding="utf-8-sig"
)

print(f"\n[SUKSES] Preprocessing SVM selesai!")
print(f"-> File disimpan sebagai: {output_file}")

# Tampilkan 5 contoh perbandingan teks asli vs teks bersih SVM
print("\nContoh Hasil Preprocessing SVM:")
for i in range(5):
  print(f"Asli  : {df.loc[i, 'review_text']}")
  print(f"Bersih: {df.loc[i, 'text_clean_svm']}")
  print("-" * 40)