import os
import pandas as pd

# Konfigurasi Direktori & Parameter Utama
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "../MergeDataset/dataset_master_gabungan_2026.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "sampel_anotasi_kappa.csv")

# Ukuran sampel untuk uji Cohen's Kappa (standar umum: 250 data)
SAMPLE_SIZE = 250
RANDOM_SEED = 42

print("PROSES SAMPLING UNTUK ANOTASI (COHEN'S KAPPA)\n")

if os.path.exists(INPUT_FILE):
  df_master = pd.read_csv(INPUT_FILE)
  total_data = len(df_master)

  # Pastikan n tidak melebihi total populasi master
  n_take = min(SAMPLE_SIZE, total_data)

  # Simple Random Sampling dari master gabungan
  df_sample = df_master.sample(n=n_take, random_state=RANDOM_SEED).reset_index(
      drop=True
  )

  # Simpan file hasil sampel anotasi
  df_sample.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

  print(f"[SUKSES]")
  print(f"  - Total Populasi Master : {total_data:,}")
  print(f"  - Sampel Terambil (n)   : {len(df_sample):,}")
  print(f"  - Output File           : {os.path.basename(OUTPUT_FILE)}")
else:
  print(
      f"[GAGAL] File '{os.path.basename(INPUT_FILE)}' tidak ditemukan."
  )