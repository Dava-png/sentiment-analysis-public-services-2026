import pandas as pd
import os

# Mengunci direktori dasar tempat skrip berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Daftar file sampel per aplikasi yang akan digabung
SAMPLE_FILES = [
    os.path.join(BASE_DIR, "../sample_mobile_jkn_2026.csv"),
    os.path.join(BASE_DIR, "sample_signal_2026.csv"),
    os.path.join(BASE_DIR, "sample_m-paspor_2026.csv")
]

sampled_datasets = []

print("=== PROSES PENGGABUNGAN DATASET MASTER (T1.4) ===\n")

for filepath in SAMPLE_FILES:
    try:
        df_sample = pd.read_csv(filepath)
        sampled_datasets.append(df_sample)
        print(f"Berhasil memuat: {os.path.basename(filepath)} ({len(df_sample):,} baris)")
    except FileNotFoundError:
        print(f"[PERINGATAN] File '{filepath}' tidak ditemukan. Pastikan skrip sampling sudah dijalankan sebelumnya.")

if sampled_datasets:
    # Menggabungkan seluruh dataframe sampel menjadi satu (concatenation)
    df_master = pd.concat(sampled_datasets, ignore_index=True)
    
    # Simpan ke file master akhir
    master_filename = "dataset_master_2026.csv"
    df_master.to_csv(master_filename, index=False, encoding="utf-8-sig")
    
    print(f"\n=== PENGGABUNGAN SELESAI ===")
    print(f"Total keseluruhan baris pada dataset master: {len(df_master):,} baris")
    print(f"Disimpan sebagai: {master_filename}")