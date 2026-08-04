import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
import re
from urllib.parse import urlparse, parse_qs

def normalize_url(url):
    """Return a canonical version of the URL."""

    url = url.strip()

    # arXiv
    if "arxiv.org" in url:
        m = re.search(r"(\d{4}\.\d{4,5})", url)
        if m:
            return f"https://arxiv.org/abs/{m.group(1)}"

    # YouTube
    if "youtu.be/" in url:
        video = url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video}"

    if "youtube.com" in url:
        qs = parse_qs(urlparse(url).query)
        if "v" in qs:
            return f"https://www.youtube.com/watch?v={qs['v'][0]}"

    # Remove query parameters from everything else
    parsed = urlparse(url)

    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

url = input("URL: ").strip()

url = normalize_url(url)

for md in Path("content").rglob("*.md"):
    text = md.read_text(encoding="utf-8")

    urls = []

    # Check YAML front matter URL
    yaml_url = re.search(
        r'^url:\s*"?(.*?)"?$',
        text,
        re.MULTILINE
    )

    if yaml_url:
        urls.append(yaml_url.group(1))

    # Check Link section for older files
    link_section = re.search(
        r'## Link\s*\n\s*(\S+)',
        text
    )

    if link_section:
        urls.append(link_section.group(1))

    for existing_url in urls:
        if normalize_url(existing_url) == url:
            print("\n⚠️ This resource already exists:")
            print(md)
            exit()

def get_title(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.title and soup.title.string:
            return soup.title.string.strip()

    except Exception:
        pass

    return None

def detect_type(url):
    url = url.lower()

    if "arxiv.org" in url:
        return "p"

    if "doi.org" in url:
        return "p"

    if "github.com" in url:
        return "g"

    if "youtube.com" in url or "youtu.be" in url:
        return "v"

    if "huggingface.co/learn" in url:
        return "c"

    if "dataverse" in url:
        return "d"

    return None

RESOURCE_TYPES = {
    "b": ("books", "Book"),
    "c": ("courses", "Course"),
    "t": ("tutorials", "Tutorial"),
    "p": ("papers", "Paper"),
    "w": ("websites", "Website"),
    "d": ("datasets", "Dataset"),
    "v": ("videos", "Video"),
    "g": ("code", "Code"),
}

print("\n📚 Learning Library - Add Resource\n")

url = input("URL: ").strip()

suggested_type = detect_type(url)

if suggested_type:
    folder, resource_type = RESOURCE_TYPES[suggested_type]

    print(f"\nDetected type: {resource_type}")

    confirm = input(
        "Press Enter to accept or type another letter: "
    ).lower().strip()

    if confirm:
        choice = confirm
    else:
        choice = suggested_type

else:
    print("\nChoose type:")
    for key, (_, name) in RESOURCE_TYPES.items():
        print(f"{key}) {name}")

    choice = input("\nType letter: ").lower().strip()


if choice not in RESOURCE_TYPES:
    print("Invalid choice")
    exit()

folder, resource_type = RESOURCE_TYPES[choice]

if choice not in RESOURCE_TYPES:
    print("Invalid choice")
    exit()

folder, resource_type = RESOURCE_TYPES[choice]

found_title = get_title(url)

if found_title:
    print(f"\nTitle found: {found_title}")
    title = input("Press Enter to accept or type a new title: ").strip()

    if not title:
        title = found_title
else:
    title = input("\nTitle: ").strip()

    if not title:
        title = urlparse(url).netloc

filename_title = re.sub(r"^\[[^\]]+\]\s*", "", title)

filename = re.sub(
    r"[^a-z0-9]+",
    "-",
    filename_title.lower()
).strip("-")

filepath = Path("content") / folder / f"{filename}.md"

filepath.parent.mkdir(parents=True, exist_ok=True)

# Avoid overwriting existing resources
if filepath.exists():
    print(f"\n⚠️ Resource already exists:")
    print(filepath)

    new_name = input(
        "Enter a different filename or press Enter to cancel: "
    ).strip()

    if new_name:
        filename = re.sub(r"[^a-z0-9]+", "-", new_name.lower()).strip("-")
        filepath = Path("content") / folder / f"{filename}.md"
    else:
        print("Cancelled.")
        exit()

safe_title = title.replace('"', '\\"')

content = f"""---
title: "{safe_title}"
type: {resource_type}
url: "{url}"
---

# {title}

## Link

{url}

## Why I saved it


## Notes


## Related resources

"""

filepath.write_text(content, encoding="utf-8")

print(f"\n✅ Created: {filepath}")
