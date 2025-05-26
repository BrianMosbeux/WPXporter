# run.py
from utils import fetch_wordpress_content, process_posts, save_json, fetch_json, export_content, process_exported_content
import json
from pathlib import Path
from config import Config


def fetch_content_sample():
    data = {}
    dir = Path('raw_json') #to updated once data folders are restructured
    for f_path in dir.iterdir():
        if f_path.is_file():
            with f_path.open('r', encoding='utf-8') as f:
                json_data = json.load(f)
                data[f_path.stem] = json_data[0]
    with open('sample_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    for key in data:
        print(f"\n##{key}\n")
        for k in data[key]:
            print(f"  - {k}")




def save_mdx_file(post, output_dir="mdx/posts"):
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    slug = post.get('slug', f"post-{post.get('id', 'unknown')}")
    filename = output_path / f"{slug}.mdx"
    
    # Safely extract fields with defaults
    meta_data = {
        "id": post.get("id", ""),
        "slug": slug,
        "date": post.get("date", ""),
        "modified": post.get("modified", ""),
        "status": post.get("status", ""),
        "title": post.get("title", ""),
        "author": post.get("author", ""),
        "featured_media": post.get("featured_media", ""),
        "categories": post.get("categories", []),
        "tags": post.get("tags", []),
        "seo": {
            "meta_description": post.get("meta_description", ""),
            "canonical": post.get("canonical", ""),
            "og": {
                "title": post.get("og_title", ""),
                "description": post.get("og_description", ""),
                "image": post.get("og_image", ""),
                "type": post.get("og_type", ""),
                "url": post.get("og_url", ""),
            },
            "twitter": {
                "card": post.get("twitter_card", ""),
                "title": post.get("twitter_title", ""),
                "description": post.get("twitter_description", ""),
                "image": post.get("twitter_image", ""),
                "creator": post.get("twitter_creator", ""),
            },
        }
    }
    
    # Convert meta_data to a JSON-formatted string with indentations
    meta_json = json.dumps(meta_data, indent=2)
    
    # Prepare MDX content
    mdx_content = f"""export const meta = {meta_json};\n\n# {post.get('title')}\n\n{post.get('content')}"""
    
    # Save to file
    with filename.open("w", encoding="utf-8") as f:
        f.write(mdx_content)
    
    print(f"✅ MDX file saved: {filename}")


if __name__ == '__main__':
    # export_content()
    # process_exported_content()
    # posts = fetch_json('posts', Config.processed_json_path)
    # for post in posts:
    #    save_mdx_file(post)

    posts = fetch_json('posts', Config.processed_json_path)

    print(len(posts))

    
