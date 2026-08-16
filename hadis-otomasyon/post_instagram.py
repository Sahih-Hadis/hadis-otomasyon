"""
docs/latest.png içindeki görseli, GitHub Pages üzerinden herkese açık
bir URL olarak Instagram Graph API'ye gönderip yayınlar.

Ortam değişkenleri (GitHub Actions Secrets'tan gelir):
    IG_ACCESS_TOKEN
    IG_BUSINESS_ACCOUNT_ID
    GITHUB_PAGES_URL   (örn: https://kullaniciadi.github.io/hadis-otomasyon)
"""
import os
import sys
import time
import requests

API_VERSION = "v21.0"


def env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Eksik ortam değişkeni: {name}")
    return value


def main():
    access_token = env("IG_ACCESS_TOKEN")
    ig_user_id = env("IG_BUSINESS_ACCOUNT_ID")
    pages_url = env("GITHUB_PAGES_URL").rstrip("/")

    image_url = f"{pages_url}/latest.png?v={int(time.time())}"

    caption_path = os.path.join(os.path.dirname(__file__), "docs", "latest_caption.txt")
    with open(caption_path, encoding="utf-8") as f:
        caption = f.read()

    # 1. Media container oluştur
    create_resp = requests.post(
        f"https://graph.facebook.com/{API_VERSION}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
    )
    create_resp.raise_for_status()
    creation_id = create_resp.json()["id"]

    # 2. Container hazır olana kadar bekle (görsel URL'den indirilip işleniyor)
    for _ in range(20):
        status_resp = requests.get(
            f"https://graph.facebook.com/{API_VERSION}/{creation_id}",
            params={"fields": "status_code", "access_token": access_token},
        )
        status = status_resp.json().get("status_code")
        if status == "FINISHED":
            break
        if status == "ERROR":
            raise SystemExit(f"Container işlenirken hata oluştu: {status_resp.json()}")
        time.sleep(5)
    else:
        raise SystemExit("Container zaman aşımına uğradı, FINISHED durumuna ulaşamadı.")

    # 3. Yayınla
    publish_resp = requests.post(
        f"https://graph.facebook.com/{API_VERSION}/{ig_user_id}/media_publish",
        data={"creation_id": creation_id, "access_token": access_token},
    )
    publish_resp.raise_for_status()
    print("Paylaşım başarılı:", publish_resp.json())


if __name__ == "__main__":
    main()
