from pathlib import Path
from datetime import date
from urllib.parse import urlparse
import re

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

print("\nChoose type:")
for key, (_, name) in RESOURCE_TYPES.items():
    print(f"{key}) {name}")

choice = input("\nType letter: ").lower().strip()

if choice not in RESOURCE_TYPES:
    print("Invalid choice")
    exit()

folder, resource_type = RESOURCE_TYPES[choice]

title = input("\nTitle: ").strip()

if not title:
    title = urlparse(url).netloc

filename = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

filepath = Path("content") / folder / f"{filename}.md"

filepath.parent.mkdir(parents=True, exist_ok=True)

content = f"""---
title: {title}
type: {resource_type}
date_added: {date.today()}
---

# {title}

## Link

{url}

## Notes


"""

filepath.write_text(content, encoding="utf-8")

print(f"\n✅ Created: {filepath}")