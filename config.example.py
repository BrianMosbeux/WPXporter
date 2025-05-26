# config.py

from pathlib import Path

class Config:
    # Set your WordPress domain here
    DOMAIN = 'https://YOURDOMAIN.COM'  # <-- Replace YOURDOMAIN.COM with your actual domain
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    PARAMS = {"per_page": 100, "page": 1} 
    DEFAULT_CONTENT_TYPES = [
        'posts', 'pages', 'media', 'categories', 'tags', 'comments', 'users'
    ]
    DATA_DIR = Path("data")
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"

    @classmethod
    def wp_api_url(cls, content_type):
        return f"https://{cls.DOMAIN}/wp-json/wp/v2/{content_type}"
    
    @classmethod
    def raw_json_path(cls, file_name):
        cls.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        return cls.RAW_DATA_DIR / f"{file_name}.json"

    @classmethod
    def processed_json_path(cls, file_name):
        cls.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        return cls.PROCESSED_DATA_DIR / f"{file_name}.json"
