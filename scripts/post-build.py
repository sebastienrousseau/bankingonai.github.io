import os, re, json, shutil

repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. Sync manifest.json
manifest_data = {
    "name": "Banking On AI",
    "short_name": "bankingonai",
    "description": "Discover how AI is transforming the banking sector with improved customer service, fraud detection, and streamlined operations.",
    "start_url": "/index.html",
    "scope": "/",
    "display": "standalone",
    "orientation": "portrait-primary",
    "background_color": "#fbfbfd",
    "theme_color": "#1d1d1f",
    "lang": "en-GB",
    "icons": [
        {
            "src": "https://cloudcdn.pro/bankingonai/v1/logos/bankingonai.svg",
            "sizes": "512x512",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        },
        {
            "src": "https://cloudcdn.pro/cmn/v1/icons/192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ]
}

for target in ["public", "docs"]:
    m_path = os.path.join(repo_dir, target, "manifest.json")
    with open(m_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

# 2. Clean up internal links and unrendered entities in all HTML output
for target in ["public", "docs"]:
    base_target = os.path.join(repo_dir, target)
    if not os.path.exists(base_target):
        continue
    for root, _, files in os.walk(base_target):
        for file in files:
            if not file.endswith(".html"):
                continue
            fpath = os.path.join(root, file)
            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()

            # Clean links
            html = html.replace('href="/about.html"', 'href="/about/index.html"')
            html = html.replace('href="/contact.html"', 'href="/contact/index.html"')
            html = html.replace('href="/features.html"', 'href="/features/index.html"')
            html = html.replace('href="/faqs.html"', 'href="/faqs/index.html"')
            html = html.replace('href="/accessibility.html"', 'href="/accessibility/index.html"')
            html = html.replace('href="/privacy.html"', 'href="/privacy/index.html"')
            html = html.replace('href="/terms.html"', 'href="/terms/index.html"')
            html = html.replace('href="/made-with-ssg.html"', 'href="/made-with-ssg/index.html"')
            html = html.replace('href="about.html"', 'href="/about/index.html"')
            html = html.replace('href="contact.html"', 'href="/contact/index.html"')
            html = html.replace('href="features.html"', 'href="/features/index.html"')

            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)

# 3. Sync static assets (favicon, images, islands)
for target in ["public", "docs"]:
    for asset in ["favicon.ico", "images", "islands"]:
        src_path = os.path.join(repo_dir, asset)
        dst_path = os.path.join(repo_dir, target, asset)
        if os.path.isfile(src_path):
            shutil.copyfile(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)

# 4. Write CNAME
cname_domain = "bankingonai.co"
for target in ["public", "docs"]:
    with open(os.path.join(repo_dir, target, "CNAME"), "w", encoding="utf-8") as f:
        f.write(cname_domain + "\n")
with open(os.path.join(repo_dir, "CNAME"), "w", encoding="utf-8") as f:
    f.write(cname_domain + "\n")

print("Post-build optimization completed with synchronized manifest, assets, CNAME, and clean links.")
