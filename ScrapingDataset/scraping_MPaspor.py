import pandas as pd
from datetime import datetime
from google_play_scraper import reviews, Sort

APP_NAME = "M-Paspor"
PACKAGE_NAME = "id.go.imigrasi.paspor_online"  # <-- Diperbarui dengan package name yang benar

# Batas awal dan akhir tahun 2026
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 12, 31, 23, 59, 59)

print(f"Memulai pengambilan ulasan untuk {APP_NAME} (Jan - Des 2026)...")

all_reviews = []
continuation_token = None
fetched_count = 0
batch_loop = 1

while True:
    try:
        result, continuation_token = reviews(
            PACKAGE_NAME,
            lang='id',
            country='id',
            sort=Sort.NEWEST,
            count=200,
            continuation_token=continuation_token
        )
    except Exception as e:
        print(f"Error koneksi pada batch {batch_loop}: {e}")
        break
    
    if not result:
        print("Ulasan dari server habis atau koneksi melambat.")
        break
        
    valid_in_batch = 0
    stop_scraping = False
    
    for r in result:
        review_date = r.get("at")
        
        if isinstance(review_date, str):
            try:
                review_date = datetime.strptime(review_date[:10], "%Y-%m-%d")
            except:
                continue
                
        if START_DATE <= review_date <= END_DATE:
            all_reviews.append({
                "app_name": APP_NAME,
                "review_id": r.get("reviewId"),
                "score": r.get("score"),
                "at": review_date.strftime("%Y-%m-%d"),
                "review_text": r.get("content")
            })
            valid_in_batch += 1
        elif review_date < START_DATE:
            stop_scraping = True
            
    fetched_count = len(all_reviews)
    print(f"Batch {batch_loop}: Menemukan {valid_in_batch} data valid (Total terkumpul: {fetched_count})")
    
    batch_loop += 1
    
    if stop_scraping:
        print("Mencapai batas tanggal sebelum tahun 2026. Selesai.")
        break
        
    if not continuation_token:
        print("Token halaman habis.")
        break

if all_reviews:
    df = pd.DataFrame(all_reviews)
    output_filename = "dataset_mpaspor_2026.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\nSelesai! Tersimpan sebagai '{output_filename}' dengan total {len(df)} data.")
else:
    print("\nPeringatan: Masih 0 data terkumpul.")