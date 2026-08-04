from pathlib import Path
import re


CONTENT_DIR = Path("content")


def extract_url(text):
    """
    Extract URL from ## Link section.
    """

    match = re.search(
        r"## Link\s*\n\s*(https?://\S+)",
        text
    )

    if match:
        return match.group(1).strip()

    return None


def add_url_to_frontmatter(filepath):

    text = filepath.read_text(encoding="utf-8")

    # Skip if URL already exists
    if re.search(r"^url:", text, re.MULTILINE):
        return False

    url = extract_url(text)

    if not url:
        return False

    # Insert URL before closing ---
    updated = re.sub(
        r"(type:\s*.*\n)(---)",
        rf"\1url: \"{url}\"\n\2",
        text,
        count=1
    )

    filepath.write_text(
        updated,
        encoding="utf-8"
    )

    return True


updated_count = 0

for file in CONTENT_DIR.rglob("*.md"):

    if file.name == "resource-template.md":
        continue

    if add_url_to_frontmatter(file):
        print(f"✓ Updated: {file}")
        updated_count += 1


print()
print(f"Done. Updated {updated_count} files.")
