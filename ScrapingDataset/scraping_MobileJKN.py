import pandas as pd
from datetime import datetime
from google_play_scraper import reviews, Sort

APP_NAME = "Mobile JKN"
PACKAGE_NAME = "app.bpjs.mobile"
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 12, 31)

print(f"Memulai pengambilan ulasan untuk {APP_NAME} (Jan - Des 2026)...")

all_reviews = []
continuation_token = None
fetched_count = 0

while True:
    result, continuation_token = reviews(
        PACKAGE_NAME,
        lang='id',
        country='id',
        sort=Sort.NEWEST,
        count=200,
        continuation_token=continuation_token
    )
    
    if not result:
        break
        
    stop_scraping = False
    for r in result:
        review_date = r.get("at")
        
        if START_DATE <= review_date <= END_DATE:
            all_reviews.append({
                "app_name": APP_NAME,
                "review_id": r.get("reviewId"),
                "score": r.get("score"),
                "at": review_date.strftime("%Y-%m-%d"),
                "review_text": r.get("content")
            })
        elif review_date < START_DATE:
            stop_scraping = True
            
    fetched_count = len(all_reviews)
    print(f"Terkumpul {fetched_count} ulasan dalam rentang waktu riset...")
    
    if stop_scraping or not continuation_token:
        break

df = pd.DataFrame(all_reviews)
df.to_csv("dataset_mobile_jkn_2026.csv", index=False, encoding='utf-8-sig')
print(f"Selesai! Tersimpan sebagai 'dataset_mobile_jkn_2026.csv' ({len(df)} data).\n")