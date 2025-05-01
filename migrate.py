import requests


# WordPress API URL
WP_API_URL = "https://{domain}/wp-json/wp/v2/{content_type}"

# Simulate a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def main(domain, content_type):
    url = WP_API_URL.format(domain=domain, content_type=content_type)
    posts = fetch_wordpress_content(url)
    print(f"\nTotal posts fetched: {len(posts)}")


def fetch_wordpress_content(wordpress_api_url):
    content = []
    page = 1
    print(f"Fetching {wordpress_api_url}...")
    while True:  
        try:
            response = requests.get(wordpress_api_url, headers=HEADERS, params={"per_page": 100, "page": page})
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            print(f"\n--- Page {page} ---")
            content.extend(data)
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {page}: {e}")
            break
    return content

def process_posts(posts):
    processed_posts = []
    for post in posts:
        processed_posts.append({
            "id": post["id"],
            "date": post["date"],  
            "modified": post["modified"],  # Important for SEO freshness
            "slug": post["slug"],
            "status": post["status"],
            "type": post["type"],
            "title": post["title"]["rendered"],  
            "content": post["content"]["rendered"],
            "excerpt": post["excerpt"]["rendered"],
            "author": post["author"],
            "featured_media": post["featured_media"],
            "categories": post["categories"],
            "tags": post["tags"],
            "yoast_head": post["yoast_head"]
        })
    return processed_posts

if __name__ == '__main__':
    domain = input('Domain Name: ').strip()
    content_type = input('Content type: ').strip()
    main(domain, content_type)


"""
