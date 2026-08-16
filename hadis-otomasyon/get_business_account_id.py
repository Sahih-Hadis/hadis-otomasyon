"""
Bu script'i SADECE BİR KEZ, kendi bilgisayarında çalıştırıp
Instagram Business Account ID'ni bulmak için kullan.

Kullanım:
    pip install requests
    python get_business_account_id.py YOUR_ACCESS_TOKEN
"""
import sys
import requests

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python get_business_account_id.py <ACCESS_TOKEN>")
        sys.exit(1)

    token = sys.argv[1]

    # Bağlı Facebook Sayfalarını listele
    resp = requests.get(
        "https://graph.facebook.com/v21.0/me/accounts",
        params={"access_token": token},
    )
    resp.raise_for_status()
    pages = resp.json().get("data", [])

    if not pages:
        print("Hiç bağlı Facebook Sayfası bulunamadı.")
        sys.exit(1)

    for page in pages:
        page_id = page["id"]
        page_name = page["name"]
        page_token = page["access_token"]

        # Bu sayfaya bağlı Instagram Business hesabını sorgula
        ig_resp = requests.get(
            f"https://graph.facebook.com/v21.0/{page_id}",
            params={
                "fields": "instagram_business_account",
                "access_token": page_token,
            },
        )
        ig_data = ig_resp.json()
        ig_account = ig_data.get("instagram_business_account")

        print(f"\nSayfa: {page_name} (ID: {page_id})")
        if ig_account:
            print(f"  -> Instagram Business Account ID: {ig_account['id']}")
            print(f"  -> Bu Sayfa'ya özel Page Access Token: {page_token}")
            print("     (Bu page_token'ı IG_ACCESS_TOKEN olarak GitHub Secrets'a ekle,")
            print("      genel token yerine bunu kullanmak daha güvenilir olur.)")
        else:
            print("  -> Bu sayfaya bağlı Instagram Business hesabı yok.")

if __name__ == "__main__":
    main()
