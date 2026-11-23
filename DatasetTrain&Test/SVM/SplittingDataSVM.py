import os
import pandas as pd
from sklearn.model_selection import train_test_split

print("SPLIT DATASET SVM 80:20")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Memuat file hasil preprocessing SVM yang sudah kamu buat sebelumnya
# (Sesuaikan nama file jika lokasinya berbeda)
input_file = os.path.join(BASE_DIR, "../../TextPreProcessing/SVM/dataset_preprocessed_svm_2026.csv")
df = pd.read_csv(input_file)
print(f"-> Berhasil memuat data preprocessed SVM: {len(df):,} baris")

# 2. Melakukan Stratified Split (80% Train : 20% Test) berdasarkan kolom 'Kategori'
print("-> Melakukan Stratified Data Splitting (80:20)...")
train_df, test_df = train_test_split(
    df, 
    test_size=0.20, 
    random_state=42, 
    stratify=df['Kategori']
)

print(f"\n[SUKSES] Pembagian data SVM selesai!")
print(f"-> Total Data Latih SVM (80%): {len(train_df):,} baris")
print(f"-> Total Data Uji SVM (20%)  : {len(test_df):,} baris")

# 3. Simpan ke dalam 2 file terpisah khusus SVM
train_file = "dataset_train_svm_80.csv"
test_file = "dataset_test_svm_20.csv"

train_df.to_csv(train_file, index=False, encoding='utf-8-sig')
test_df.to_csv(test_file, index=False, encoding='utf-8-sig')

print(f"\n-> File Train SVM disimpan sebagai : {train_file}")
print(f"-> File Test SVM disimpan sebagai  : {test_file}")