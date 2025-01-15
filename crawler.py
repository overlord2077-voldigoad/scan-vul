
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def run_crawler(base_url, config, depth=0, visited=None):
    if visited is None:
        visited = set()

    max_depth = config.get("crawler", {}).get("max_depth", 2)
    if depth > max_depth:
        return []

    if base_url in visited:
        return []

    visited.add(base_url)
    urls_encontradas = [base_url]

    try:
        timeout = config["requests"]["timeout"]
        verify_ssl = config["requests"].get("verify_ssl", True)
        headers = config["requests"].get("headers", {})
        r = requests.get(base_url, headers=headers, timeout=timeout, verify=verify_ssl)
        if r.status_code == 200 and "text/html" in r.headers.get("Content-Type", ""):
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.find_all("a", href=True)
            for link in links:
                href = link["href"]
                full_url = urljoin(base_url, href)
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    urls_encontradas.extend(run_crawler(full_url, config, depth+1, visited))
    except Exception:
        pass

    return list(set(urls_encontradas))
