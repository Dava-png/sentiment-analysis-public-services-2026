import os
import pandas as pd

# Mengunci direktori dasar tempat skrip berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANING_DIR = os.path.abspath(os.path.join(BASE_DIR, "../CleaningDataset"))

CLEAN_FILES = {
    "Mobile JKN": os.path.join(CLEANING_DIR, "clean_mobile_jkn_2026.csv"),
    "SIGNAL": os.path.join(CLEANING_DIR, "clean_signal_2026.csv"),
    "M-Paspor": os.path.join(CLEANING_DIR, "clean_m-paspor_2026.csv"),
}

TARGET_SAMPLE_LARGE = 1500  # Kuota sampel
RANDOM_SEED = 42

print("=== PROSES SRA MANUAL LOOP (DIJAMIN AMAN) ===\n")

for app_name, filepath in CLEAN_FILES.items():
  df_clean = pd.read_csv(filepath)
  total_bersih = len(df_clean)

  # Pastikan kolom score bertipe numerik
  df_clean["score"] = pd.to_numeric(df_clean["score"], errors="coerce")

  if total_bersih > TARGET_SAMPLE_LARGE:
    # SRA Proporsional menggunakan perulangan manual per nilai score (1 sampai 5)
    sampled_groups = []

    for score_val, group in df_clean.groupby("score"):
      # Hitung kuota proporsional untuk strata score ini
      n_strata = max(
          1, int(round(TARGET_SAMPLE_LARGE * len(group) / total_bersih))
      )
      # Ambil sampel acak dari kelompok score tersebut (pastikan tidak melebihi jumlah data kelompok)
      n_take = min(n_strata, len(group))
      sub_sample = group.sample(n=n_take, random_state=RANDOM_SEED)
      sampled_groups.append(sub_sample)

    # Gabungkan kembali semua strata
    df_sample = pd.concat(sampled_groups).reset_index(drop=True)
    metode = "Stratified Random Sampling / SRA (Manual Loop)"
  else:
    df_sample = df_clean.copy()
    metode = "Total Sampling / Sensus (< 1.500 data)"

  # Simpan hasil sampel per aplikasi
  sample_filename = (
      f"sample_{app_name.lower().replace(' ', '_').replace('-', '_')}_2026.csv"
  )
  df_sample.to_csv(sample_filename, index=False, encoding="utf-8-sig")

  # Validasi instan dari file CSV yang baru dibuat
  df_check = pd.read_csv(sample_filename)
  ada_score = "score" in df_check.columns
  jumlah_baris_csv = len(df_check)
  contoh_score = df_check["score"].head(3).tolist() if ada_score else "TIDAK ADA"

  print(f"[{app_name}]")
  print(f"  - Metode         : {metode}")
  print(f"  - Total Populasi : {total_bersih:,}")
  print(f"  - Sampel Terambil: {jumlah_baris_csv:,}")
  print(f"  - Kolom Score Ada: {ada_score} | Contoh: {contoh_score}")
  print(f"  - File Output    : {sample_filename}\n")

print("PROSES SELESAI. Silakan cek terminal di atas.")