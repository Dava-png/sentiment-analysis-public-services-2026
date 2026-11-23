import os
import pandas as pd
from sklearn.model_selection import train_test_split

print("SPLIT DATASET INDOBERT 80:20")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Memuat file hasil preprocessing IndoBERT yang sudah ada
input_file = os.path.join(BASE_DIR, "../../TextPreProcessing/IndoBERT/dataset_preprocessed_indobert_2026.csv")
df = pd.read_csv(input_file)
print(f"-> Berhasil memuat data preprocessed IndoBERT: {len(df):,} baris")

# 2. Melakukan Stratified Split (80% Train : 20% Test) berdasarkan kolom 'Kategori'
print("-> Melakukan Stratified Data Splitting (80:20)...")
train_df, test_df = train_test_split(
    df, 
    test_size=0.20, 
    random_state=42, 
    stratify=df['Kategori']
)

print(f"\n[SUKSES] Pembagian data IndoBERT selesai!")
print(f"-> Total Data Latih IndoBERT (80%): {len(train_df):,} baris")
print(f"-> Total Data Uji IndoBERT (20%)  : {len(test_df):,} baris")

# 3. Simpan ke dalam 2 file terpisah khusus IndoBERT
train_file = "dataset_train_indobert_80.csv"
test_file = "dataset_test_indobert_20.csv"

train_df.to_csv(train_file, index=False, encoding='utf-8-sig')
test_df.to_csv(test_file, index=False, encoding='utf-8-sig')

print(f"\n-> File Train IndoBERT disimpan sebagai : {train_file}")
print(f"-> File Test IndoBERT disimpan sebagai  : {test_file}")