# Hadis Paylaşım Otomasyonu

`hadisler.csv` içindeki listeden her gün sırayla bir hadis alır,
`templates/hadis_template.html` şablonuna yerleştirip görsel üretir
ve Instagram hesabına (Graph API ile) otomatik paylaşır.

## Kurulum sırası

1. **GitHub Pages'i etkinleştir**: Settings > Pages > Source: `main` branch, `/docs` klasörü.
2. **Secrets ekle** (Settings > Secrets and variables > Actions):
   - `IG_ACCESS_TOKEN`
   - `IG_BUSINESS_ACCOUNT_ID`
3. **Variable ekle** (aynı sayfada "Variables" sekmesi):
   - `GITHUB_PAGES_URL` → örn. `https://kullaniciadi.github.io/hadis-otomasyon`
4. `hadisler.csv` dosyasını gerçek hadis listesiyle doldur.
5. Workflow'u Actions sekmesinden manuel çalıştırıp (`workflow_dispatch`) test et.

## Dosyalar

- `hadisler.csv` — hadis veritabanı
- `templates/hadis_template.html` — görsel şablonu
- `generate_image.py` — görsel üretim scripti
- `post_instagram.py` — Instagram paylaşım scripti
- `state.json` — sıradaki hadis takibi (otomatik oluşur/güncellenir)
- `.github/workflows/daily-post.yml` — günlük zamanlama
