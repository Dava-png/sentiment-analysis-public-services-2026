import pandas as pd

# Sesuaikan nama file CSV mentah Anda di sini
FILES = {
    "Mobile JKN": "dataset_mobile_jkn_2026.csv",
    "SIGNAL": "dataset_signal_2026.csv",
    "M-Paspor": "dataset_mpaspor_2026.csv"
}

print("=== LAPORAN AUDIT DATA CLEANING & DEDUPLIKASI (T1.2) ===\n")

for app_name, filepath in FILES.items():
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"[{app_name}] File '{filepath}' tidak ditemukan. Lewatkan.")
        continue
        
    awal = len(df)
    
    # Deteksi otomatis kolom teks ulasan (review_text atau content)
    text_col = "review_text" if "review_text" in df.columns else "content"
    
    # a. Hapus baris dengan teks ulasan atau score kosong (NaN)
    df = df.dropna(subset=[text_col, "score"]).copy()
    
    # b. Hapus duplikat berdasarkan review_id / reviewId (jika kolom ada)
    if "review_id" in df.columns:
        df = df.drop_duplicates(subset=["review_id"], keep="first")
        
    # c. Pastikan bertipe string, rapikan spasi, dan buang baris yang tidak memiliki huruf/angka valid
    df[text_col] = df[text_col].astype(str).str.strip()
    df = df[df[text_col].str.contains(r'[a-zA-Z0-9]', regex=True)]
    
    # Standarisasi nama kolom menjadi 'review_text' dan pastikan kolom 'app_name' ada
    df = df.rename(columns={text_col: "review_text"})
    df["app_name"] = app_name
    
    bersih = len(df)
    terhapus = awal - bersih
    
    print(f"[{app_name}]")
    print(f"  - Jumlah data awal (mentah)   : {awal:,}")
    print(f"  - Data kosong/duplikat/sampah : -{terhapus:,}")
    print(f"  - Sisa data bersih valid      : {bersih:,}\n")
    
    # Simpan hasil pembersihan ke file CSV baru khusus versi bersih
    clean_filename = f"clean_{app_name.lower().replace(' ', '_')}_2026.csv"
    df.to_csv(clean_filename, index=False, encoding="utf-8-sig")

print("=== SEMUA DATA BERSIH BERHASIL DISIMPAN PER APLIKASI ===")