import requests
from bs4 import BeautifulSoup


def extract_website_data(url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return {"error": "Failed to fetch webpage"}

        html = response.text

    except Exception:
        return {"error": "Failed to load page"}

    soup = BeautifulSoup(html, "html.parser")

    # Title
    title = soup.title.string if soup.title else ""

    # Meta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")

    # Headings
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text:
            headings.append(text)

    # Paragraphs
    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text and len(text) > 40:
            paragraphs.append(text)

    # Links
    links = []
    for link in soup.find_all("a", href=True):
        links.append(link["href"])

    full_text = " ".join(paragraphs)

    # FAQ detection
    faq_detected = False
    for h in headings:
        if "faq" in h.lower() or "frequently asked" in h.lower():
            faq_detected = True

    return {
        "title": title,
        "meta_description": meta_desc,
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links,
        "text": full_text[:8000],
        "faq_detected": faq_detected
    }