import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
import re

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

filename = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

filepath = Path("content") / folder / f"{filename}.md"

filepath.parent.mkdir(parents=True, exist_ok=True)

content = f"""---
title: {title}
type: {resource_type}
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
