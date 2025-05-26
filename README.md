# WPXporter

**WPXporter** is a Python-based tool that exports WordPress content into **MDX**, **Markdown**, and **JSON** formats.
It’s perfect for migrating your blog to a modern web framework (like Next.js) or simply backing up your WordPress content efficiently.

## 🚀 Features

* Export WordPress posts and pages.
* Supports **MDX**, **Markdown**, and **JSON** output formats.
* Preserves categories, tags, featured images, and metadata.
* Cleans up formatting and converts HTML into Markdown-friendly content.
* Easy to extend and customize for additional formats.

## 📦 Installation

```bash
git clone https://github.com/BrianMosbeux/WPXporter.git
cd WPXporter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Usage

1. Rename `example.config.py` to `config.py` and replace `<YOURDOMAIN.COM>` with your actual WordPress domain.
2. Export your content:

```bash
python run.py
```

3. Access your exported files:

* `data/raw/` - raw WordPress JSON content
* `data/processed/` - cleaned JSON content
* `mdx/posts/` - converted MDX files for posts

## 🏗️ Future Plans

* **Restructure project**
* **Add support for additional formats** (e.g., MD, YAML, CSV).
* **Extend export options** (e.g., custom post types, selective exports).
* **Add CLI arguments** for easier customization.

## 🧑‍💻 Contributing

Contributions are welcome!
Feel free to fork the repository, submit pull requests, or open issues to suggest improvements.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Created with ❤️ by **Brian Mosbeux**

---
