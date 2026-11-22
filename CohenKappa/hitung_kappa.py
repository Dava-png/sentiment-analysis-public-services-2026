import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix, classification_report

# Konfigurasi Direktori
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path file anotasi kedua annotator
file_dava = os.path.join(BASE_DIR, "../AnotasiDuaOrang/sampel_anotasi_kappa(Dava).csv")
file_alen = os.path.join(BASE_DIR, "../AnotasiDuaOrang/sampel_anotasi_kappa(Alen).csv")

print("=== PENGUJIAN RELIABILITAS COHEN'S KAPPA ===\n")

if os.path.exists(file_dava) and os.path.exists(file_alen):
    df_dava = pd.read_csv(file_dava)
    df_alen = pd.read_csv(file_alen)

    col_name = "Kategori" 

    if col_name in df_dava.columns and col_name in df_alen.columns:
        # Ambil nilai label dari kedua annotator
        y_dava = df_dava[col_name]
        y_alen = df_alen[col_name]

        # Hitung Cohen's Kappa Score
        kappa_score = cohen_kappa_score(y_dava, y_alen)

        print(f"Total Sampel Teranotasi : {len(df_dava):,}")
        print(f"Skor Cohen's Kappa      : {kappa_score:.4f}")
        
        # Interpretasi standar nilai Cohen's Kappa
        if kappa_score > 0.80:
            interpretasi = "Sangat Kuat (Almost Perfect Agreement)"
        elif kappa_score > 0.60:
            interpretasi = "Kuat (Substantial Agreement)"
        elif kappa_score > 0.40:
            interpretasi = "Sedang (Moderate Agreement)"
        else:
            interpretasi = "Lemah (Fair/Poor Agreement)"
            
        print(f"Interpretasi Kesepakatan: {interpretasi}\n")
        
        # Opsional: Menampilkan Confusion Matrix perbandingan antar annotator
        print("Confusion Matrix (Dava vs Alen):")
        print(confusion_matrix(y_dava, y_alen))
    else:
        print(f"[ERROR] Kolom '{col_name}' tidak ditemukan pada salah satu file CSV.")
        print(f"Kolom Dava : {df_dava.columns.tolist()}")
        print(f"Kolom Alen : {df_alen.columns.tolist()}")
else:
    print("[ERROR] Salah satu atau kedua file CSV anotasi tidak ditemukan di direktori!")