from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def extract_website_data(url):

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
            except:
                browser.close()
                return {"error": "Page load timeout or blocked by website"}

            # allow dynamic content to load
            page.wait_for_timeout(3000)

            html = page.content()

            browser.close()

    except:
        return {"error": "Failed to start browser or load page"}

    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)

    # Meta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta["content"]

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
    for a in soup.find_all("a", href=True):
        links.append(a["href"])

    # Combine text
    full_text = " ".join(paragraphs)

    # Detect FAQ section
    faq_detected = False
    for h in headings:
        if "faq" in h.lower() or "frequently asked" in h.lower():
            faq_detected = True

    data = {
        "title": title,
        "meta_description": meta_desc,
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links,
        "text": full_text[:8000],  # limit size for LLM
        "faq_detected": faq_detected
    }

    return data