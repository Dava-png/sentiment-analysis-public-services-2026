import os
import pandas as pd

# Konfigurasi Direktori Dasar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Daftar file sampel per aplikasi yang akan digabung
SAMPLE_FILES = {
    "Mobile JKN": os.path.join(BASE_DIR, "../SamplingDataset/sample_mobile_jkn_2026.csv"),
    "SIGNAL": os.path.join(BASE_DIR, "../SamplingDataset/sample_signal_2026.csv"),
    "M-Paspor": os.path.join(BASE_DIR, "../SamplingDataset/sample_m_paspor_2026.csv"),
}

print("=== PROSES MERGE DATASET SAMPEL ===\n")

dfs = []
for app_name, filepath in SAMPLE_FILES.items():
  if os.path.exists(filepath):
    df_temp = pd.read_csv(filepath)
    dfs.append(df_temp)
    print(f"[{app_name}] Berhasil dimuat: {len(df_temp):,} baris")
  else:
    print(
        f"[{app_name}] [GAGAL] File tidak ditemukan di path: {filepath}. Pastikan"
        " tahap sampling sudah dijalankan!"
    )

if dfs:
  # Gabungkan seluruh dataframe sampel secara vertikal
  df_master = pd.concat(dfs, ignore_index=True)

  # Mengacak baris (shuffling) agar data dari berbagai aplikasi tercampur merata
  df_master = df_master.sample(frac=1, random_state=42).reset_index(drop=True)

  # Simpan sebagai file master gabungan
  output_filename = "dataset_master_gabungan_2026.csv"
  output_path = os.path.join(BASE_DIR, output_filename)
  df_master.to_csv(output_path, index=False, encoding="utf-8-sig")

  print(f"\n[SUKSES] Penggabungan Selesai!")
  print(f"  - Total Keseluruhan Data : {len(df_master):,}")
  print(f"  - Disimpan sebagai       : {output_filename}")
else:
  print(
      "\n[GAGAL TOTAL] Tidak ada file sampel yang dapat digabungkan. Periksa"
      " kembali file sumbernya."
  )