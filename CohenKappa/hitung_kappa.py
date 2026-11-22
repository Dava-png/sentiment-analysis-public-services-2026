import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

# Konfigurasi Direktori
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_dava = os.path.join(BASE_DIR, "../AnotasiDuaOrang/sampel_anotasi_kappa(Dava).csv")
file_alen = os.path.join(BASE_DIR, "../AnotasiDuaOrang/sampel_anotasi_kappa(Alen).csv")

print("=== PENGUJIAN RELIABILITAS COHEN'S KAPPA ===\n")

if os.path.exists(file_dava) and os.path.exists(file_alen):
  df_dava = pd.read_csv(file_dava)
  df_alen = pd.read_csv(file_alen)

  # Kolom label sesuai file kalian
  col_dava = "Kategori"
  col_alen = "Kategori"


  def standardize_label(val):
    if pd.isna(val):
      return "Unknown"
    return str(val).strip().capitalize()


  if col_dava in df_dava.columns and col_alen in df_alen.columns:
    y_dava = df_dava[col_dava].apply(standardize_label)
    y_alen = df_alen[col_alen].apply(standardize_label)

    # Hitung Cohen's Kappa
    kappa_score = cohen_kappa_score(y_dava, y_alen)

    print(f"Total Sampel Teranotasi : {len(df_dava):,}")
    print(f"Skor Cohen's Kappa      : {kappa_score:.4f}")

    # Interpretasi
    if kappa_score > 0.80:
      interpretasi = "Sangat Kuat (Almost Perfect Agreement)"
    elif kappa_score > 0.60:
      interpretasi = "Kuat (Substantial Agreement)"
    elif kappa_score > 0.40:
      interpretasi = "Sedang (Moderate Agreement)"
    else:
      interpretasi = "Lemah (Fair/Poor Agreement)"

    print(f"Interpretasi Kesepakatan: {interpretasi}\n")

    # Confusion Matrix dengan Label Kelas yang Jelas
    labels_order = ["Positif", "Netral", "Negatif"]
    cm = confusion_matrix(y_dava, y_alen, labels=labels_order)

    # Cetak dalam format tabel rapi
    print("CONFUSION MATRIX (Baris = Dava, Kolom = Alen):")
    print(f"{'':<10} | {'Positif':<8} | {'Netral':<8} | {'Negatif':<8}")
    print("-" * 44)
    for i, label in enumerate(labels_order):
      print(
          f"{label:<10} | {cm[i][0]:<8} | {cm[i][1]:<8} | {cm[i][2]:<8}"
      )
  else:
    print("[ERROR] Nama kolom tidak ditemukan!")
else:
    print("[ERROR] File CSV tidak ditemukan!")