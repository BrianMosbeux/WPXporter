from bs4 import BeautifulSoup
import os
import json
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
    processed_posts = process_posts(posts)
    print(f"\nTotal posts processed: {len(processed_posts)}")
    save_to_json(processed_posts)

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
        seo_data = extract_seo_metadata(post["yoast_head"])
        processed_posts.append({
            "id": post["id"],
            "date": post["date"],  
            "modified": post["modified"],  # Important for SEO freshness
            "slug": post["slug"],
            "status": post["status"],
            "type": post["type"],
            "link": post["link"],
            "title": post["title"]["rendered"],  
            "content": post["content"]["rendered"],
            "excerpt": post["excerpt"]["rendered"],
            "author": post["author"],
            "featured_media": post["featured_media"],
            "categories": post["categories"],
            "tags": post["tags"],
            **seo_data
        })
    return processed_posts

def extract_seo_metadata(yoast_head):
    soup = BeautifulSoup(yoast_head, 'html.parser')
    seo_data = {
        "meta_description": None,
        "canonical": None,
        "og_title": None,
        "og_description": None,
        "og_image": None,
        "og_url": None,
        "og_type": None,
        "og_site_name": None,
        "twitter_card": None,
        "twitter_title": None,
        "twitter_description": None,
        "twitter_image": None,
        "twitter_creator": None,
        "structured_data": None
    }
    # Extract meta tags
    description_tag = soup.find("meta", {"name": "description"})
    if description_tag:
        seo_data["meta_description"] = description_tag.get("content")
    canonical_tag = soup.find("link", {"rel": "canonical"})
    if canonical_tag:
        seo_data["canonical"] = canonical_tag.get("href")
    og_title_tag = soup.find("meta", {"property": "og:title"})
    if og_title_tag:
        seo_data["og_title"] = og_title_tag.get("content")
    og_description_tag = soup.find("meta", {"property": "og:description"})
    if og_description_tag:
        seo_data["og_description"] = og_description_tag.get("content")
    og_image_tag = soup.find("meta", {"property": "og:image"})
    if og_image_tag:
        seo_data["og_image"] = og_image_tag.get("content")
    og_url_tag = soup.find("meta", {"property": "og:url"})
    if og_url_tag:
        seo_data["og_url"] = og_url_tag.get("content")
    og_type_tag = soup.find("meta", {"property": "og:type"})
    if og_type_tag:
        seo_data["og_type"] = og_type_tag.get("content")
    og_site_name_tag = soup.find("meta", {"property": "og:site_name"})
    if og_site_name_tag:
        seo_data["og_site_name"] = og_site_name_tag.get("content")
    twitter_card_tag = soup.find("meta", {"name": "twitter:card"})
    if twitter_card_tag:
        seo_data["twitter_card"] = twitter_card_tag.get("content")
    twitter_title_tag = soup.find("meta", {"name": "twitter:title"})
    if twitter_title_tag:
        seo_data["twitter_title"] = twitter_title_tag.get("content")
    twitter_description_tag = soup.find("meta", {"name": "twitter:description"})
    if twitter_description_tag:
        seo_data["twitter_description"] = twitter_description_tag.get("content")
    twitter_image_tag = soup.find("meta", {"name": "twitter:image"})
    if twitter_image_tag:
        seo_data["twitter_image"] = twitter_image_tag.get("content")
    twitter_creator_tag = soup.find("meta", {"name": "twitter:creator"})
    if twitter_creator_tag:
        seo_data["twitter_creator"] = twitter_creator_tag.get("content")
    # Extract structured data
    json_ld_tag = soup.find("script", {"type": "application/ld+json"})
    if json_ld_tag:
        try:
            seo_data["structured_data"] = json.loads(json_ld_tag.string)
        except json.JSONDecodeError:
            seo_data["structured_data"] = None
    return seo_data

def save_to_json(posts, filename="output/wordpress_posts.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    domain = input('Domain Name: ').strip()
    content_type = input('Content type: ').strip()
    main(domain, content_type)