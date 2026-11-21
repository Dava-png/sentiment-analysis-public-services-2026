import pandas as pd
import os

# Mengunci direktori dasar tempat skrip berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File data bersih hasil cleaning sebelumnya
CLEAN_FILES = {
    "Mobile JKN": os.path.join(BASE_DIR, "../CleaningDataset/clean_mobile_jkn_2026.csv"),
    "SIGNAL": os.path.join(BASE_DIR, "../CleaningDataset/clean_signal_2026.csv"),
    "M-Paspor": os.path.join(BASE_DIR, "../CleaningDataset/clean_m-paspor_2026.csv")
}

TARGET_SAMPLE_LARGE = 1500  # Kuota sampel untuk Mobile JKN & SIGNAL
RANDOM_SEED = 42

print("=== LAPORAN PROSES SAMPLING DATA (T1.3) ===\n")

for app_name, filepath in CLEAN_FILES.items():
    try:
        df_clean = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"[{app_name}] File bersih '{filepath}' tidak ditemukan. Pastikan cleaning.py sudah dijalankan.")
        continue
        
    total_bersih = len(df_clean)
    
    if total_bersih > TARGET_SAMPLE_LARGE:
        # Stratified Random Sampling proporsional berdasarkan skor bintang (score)
        df_sample = df_clean.groupby("score", group_keys=False).apply(
            lambda x: x.sample(
                n=max(1, int(round(TARGET_SAMPLE_LARGE * len(x) / total_bersih))),
                random_state=RANDOM_SEED
            )
        )
        metode = "Stratified Random Sampling (Proporsional)"
    else:
        # Total Sampling / Sensus (100% data) karena populasi di bawah 1.500
        df_sample = df_clean.copy()
        metode = "Total Sampling / Sensus (100% Data)"
    
    # Simpan sampel per aplikasi secara mandiri
    sample_filename = f"sample_{app_name.lower().replace(' ', '_')}_2026.csv"
    df_sample.to_csv(sample_filename, index=False, encoding="utf-8-sig")
    
    print(f"[{app_name}]")
    print(f"  - Metode yang digunakan : {metode}")
    print(f"  - Jumlah populasi bersih: {total_bersih:,}")
    print(f"  - Jumlah sampel terambil: {len(df_sample):,} data")
    print(f"  - Disimpan sebagai      : {sample_filename}\n")

print("PROSES SAMPLING PER APLIKASI SELESAI")