import requests
from bs4 import BeautifulSoup

def extract_instagram_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "❌ خطا در دریافت صفحه"

        soup = BeautifulSoup(response.text, "html.parser")
        video_tag = soup.find("meta", property="og:video")
        if video_tag and video_tag["content"]:
            return video_tag["content"]

        return "❌ ویدیویی یافت نشد یا این پست خصوصی است"

    except Exception as e:
        return f"⚠️ خطا: {str(e)}"
