
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape

FEED = "https://science.nasa.gov/feed/apod-basic/"
FOLDER = "Astro_Images"


def get(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "SpaceWeather/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    os.makedirs(FOLDER, exist_ok=True)

    root = ET.fromstring(get(FEED))
    item = root.find(".//item")

    if item is None:
        raise RuntimeError("No APOD entry found")

    def field(name):
        node = item.find(name)
        return node.text.strip() if node is not None and node.text else ""

    title = field("title")
    description = field("description")
    date = field("pubDate")
    page = field("link")

    # Find the image in the RSS content
    content = item.find(
        "{http://purl.org/rss/1.0/modules/content/}encoded"
    )
    html = content.text if content is not None else description

    match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE
    )

    if not match:
        raise RuntimeError("No APOD image found in RSS entry")

    image_url = unescape(match.group(1))

    if "nasa-logo" in image_url.lower():
        raise RuntimeError("NASA logo detected; keeping previous image")

    image = get(image_url)

    # Validate that the download is an actual image
    if not (
        image.startswith(b"\xff\xd8") or
        image.startswith(b"\x89PNG") or
        image.startswith(b"RIFF")
    ):
        raise RuntimeError("Downloaded file is not a valid image")

    path = os.path.join(FOLDER, "image.jpg")
    temp = path + ".tmp"

    with open(temp, "wb") as f:
        f.write(image)

    os.replace(temp, path)

    with open(os.path.join(FOLDER, "image_log.txt"), "w",
              encoding="utf-8") as f:
        f.write(f"**Date image released:** {date}\n")
        f.write(f"**Title of the image:** {title}\n")
        f.write(f"**Description for the image:** {description}\n")
        f.write(f"**URL for this image:** {image_url}\n")
        f.write(f"**NASA APOD page:** {page}\n")

    print("APOD successfully updated:", title)


if __name__ == "__main__":
    main()
