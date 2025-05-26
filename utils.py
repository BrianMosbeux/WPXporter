# utils.py
import requests
import json
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from config import Config


def export_content(content_types=None):
    if content_types is None:
        content_types = Config.DEFAULT_CONTENT_TYPES
    total_fetched = {}
    for content_type in content_types:
        url = Config.wp_api_url(content_type=content_type)
        print(f"Fetching {url}...")
        content = fetch_wordpress_content(url)
        save_json(content, content_type, Config.raw_json_path)
        total_fetched[content_type] = len(content)
        print(f"\nTotal {content_type} fetched: {len(content)}")
    print("\n Fetch Summary:")
    for ct, count in total_fetched.items():
        print(f" - {ct}: {count}")
    return total_fetched


def fetch_wordpress_content(wordpress_api_url):
    content = []
    page = 1
    while True:
        try:
            params = Config.PARAMS.copy()
            params["page"] = page
            response = requests.get(wordpress_api_url, headers=Config.HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            print(f"\n--- Page {page} ---")
            content.extend(data)
            total_pages = int(response.headers.get('X-WP-TotalPages', 1))
            if page >= total_pages:
                break
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {page}: {e}")
            break
    return content


def save_json(content, f_name, path_func):
    file = path_func(f_name)
    with file.open(mode='w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)



def fetch_json(f_name, path_func):
    file = path_func(f_name)
    with file.open(mode='r', encoding='utf-8') as f:
        content = json.load(f)
    return content


def process_exported_content(content_types=None):
    content_map = {
        'posts': process_post,
        'pages': process_page,
        'media': process_media,
        'categories': process_category,
        'tags': process_tag,
        'comments': process_comment,
        'users': process_user,
    }
    if content_types is None:
        content_types = Config.DEFAULT_CONTENT_TYPES
    for content_type in content_types:
        raw_content = fetch_json(content_type, Config.raw_json_path)
        processed_content = process_raw_content(raw_content, content_map[content_type])
        save_json(processed_content, content_type, Config.processed_json_path)


def process_raw_content(raw_content, process_content_item_func):
    processed_content = []
    for content_item in raw_content:
        processed_item = process_content_item_func(content_item)
        processed_content.append(processed_item)
    return processed_content
    


def process_posts(posts):
    processed_posts = []
    for post in posts:
        processed_post = process_post(post)
        processed_posts.append(processed_post)
    return processed_posts


def process_raw_content_item(item, fields, markdown_fields=None):
    seo_data = extract_seo_metadata(item.get("yoast_head", ""))
    processed = {field: item.get(field) for field in fields}
    if markdown_fields:
        for field in markdown_fields:
            processed[field] = md(item.get(field, {}).get("rendered"))
    processed.update(**seo_data)
    return processed


def process_category(category):
    fields = [
        "id",
        "count",
        "description",
        "link",
        "name",
        "slug",
        "parent",
    ]
    return process_raw_content_item(category, fields)


def process_comment(comment):
    fields = [
        "id",
        "post",
        "parent",
        "author",
        "author_name",
        "author_url",
        "date",
        "date_gmt",
        "link",
        "status",
        "type",
        "author_avatar_urls",
    ]
    markdown_fields = ["content"]
    return process_raw_content_item(comment, fields, markdown_fields)


def process_media(media):
    fields = [
        "id",
        "date",
        "date_gmt",  
        "modified",  
        "modified_gmt",  
        "slug",
        "type",
        "link",
        "author",
        "caption",
        "alt_text",
        "media_type",
        "mime_type",
        "media_details",
        "post",
        "source_url",
    ]
    markdown_fields = ["description", "title"]
    return process_raw_content_item(media, fields, markdown_fields)


def process_post(post):
    fields = [
        "id",
        "date",  
        "date_gmt",  
        "modified",  
        "modified_gmt",  
        "slug",
        "status",
        "type",
        "link",
        "author",
        "featured_media",
        "comment_status",
        "sticky",
        "categories",
        "tags",
    ]
    markdown_fields = ["title", "content", "excerpt"]
    return process_raw_content_item(post, fields, markdown_fields)


def process_page(page):
    fields = [
        "id",
        "date",
        "date_gmt",
        "modified",
        "modified_gmt",
        "slug",
        "status",
        "type",
        "link",
        "author",
        "featured_media",
        "parent",
        "menu_order",
        "comment_status",
        "template",
    ]
    markdown_fields = ["title", "content", "excerpt"]
    return process_raw_content_item(page, fields, markdown_fields)


def process_tag(tag):
    fields = [
        "id",
        "count",
        "description",
        "link",
        "name",
        "slug",
    ]
    return process_raw_content_item(tag, fields)


def process_user(user):
    fields = [
        "id",
        "name",
        "url",
        "description",
        "link",
        "slug",
        "avatar_urls",
    ]
    return process_raw_content_item(user, fields)


def extract_seo_metadata(yoast_head):
    soup = BeautifulSoup(yoast_head, 'html.parser')
    seo_data = {
        "meta_description": None,
        "canonical": None,
        "robots": None,
        "og_locale": None,
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
    }

    # Mapping of keys to (tag type, attribute name, attr value)
    meta_map = {
        "meta_description": ("meta", "name", "description"),
        "canonical": ("link", "rel", "canonical"),
        "robots": ("meta", "name", "robots"),
        "og_locale": ("meta", "property", "og:locale"),
        "og_title": ("meta", "property", "og:title"),
        "og_description": ("meta", "property", "og:description"),
        "og_image": ("meta", "property", "og:image"),
        "og_url": ("meta", "property", "og:url"),
        "og_type": ("meta", "property", "og:type"),
        "og_site_name": ("meta", "property", "og:site_name"),
        "twitter_card": ("meta", "name", "twitter:card"),
        "twitter_title": ("meta", "name", "twitter:title"),
        "twitter_description": ("meta", "name", "twitter:description"),
        "twitter_image": ("meta", "name", "twitter:image"),
        "twitter_creator": ("meta", "name", "twitter:creator"),
    }
    for key, (tag, attr_name, attr_value) in meta_map.items():
        element = soup.find(tag, {attr_name: attr_value})
        if element:
            if tag == "link":
                seo_data[key] = element.get("href")
            else:
                seo_data[key] = element.get("content")
    return seo_data


def extract_seo_metadata_legacy(yoast_head):
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

