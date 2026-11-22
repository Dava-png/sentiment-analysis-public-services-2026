import os
import pandas as pd

# Konfigurasi Direktori & Parameter Utama
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANING_DIR = os.path.abspath(os.path.join(BASE_DIR, "../CleaningDataset"))

DATASETS = {
    "Mobile JKN": os.path.join(CLEANING_DIR, "clean_mobile_jkn_2026.csv"),
    "SIGNAL": os.path.join(CLEANING_DIR, "clean_signal_2026.csv"),
    "M-Paspor": os.path.join(CLEANING_DIR, "clean_m-paspor_2026.csv"),
}

TARGET_SAMPLE_LARGE = 1500
RANDOM_SEED = 42

print("=== PROSES STRATIFIED RANDOM SAMPLING (SRA) ===\n")

for app_name, filepath in DATASETS.items():
  df = pd.read_csv(filepath)
  total_populasi = len(df)

  # Pastikan kolom score bertipe numerik
  df["score"] = pd.to_numeric(df["score"], errors="coerce")

  # Logika SRA vs Sensus
  if total_populasi > TARGET_SAMPLE_LARGE:
    sampled_strata = []
    for _, group in df.groupby("score"):
      # Rumus Alokasi Proporsional SRA
      n_strata = max(
          1, int(round(TARGET_SAMPLE_LARGE * len(group) / total_populasi))
      )
      sampled_strata.append(
          group.sample(n=min(n_strata, len(group)), random_state=RANDOM_SEED)
      )
    df_sample = pd.concat(sampled_strata).reset_index(drop=True)
    metode = "Stratified Random Sampling (SRA)"
  else:
    df_sample = df.copy()
    metode = "Total Sampling / Sensus (< 1.500 data)"

  # Simpan file hasil sampling
  filename = f"sample_{app_name.lower().replace(' ', '_').replace('-', '_')}_2026.csv"
  df_sample.to_csv(filename, index=False, encoding="utf-8-sig")

  # Ringkasan Eksekusi Bersih
  print(f"[{app_name}]")
  print(f"  - Metode        : {metode}")
  print(f"  - Populasi Awal : {total_populasi:,}")
  print(f"  - Sampel Terambil: {len(df_sample):,}")
  print(f"  - Output File   : {filename}\n")

print("SEMUA SAMPLING BERHASIL DIPROSES")