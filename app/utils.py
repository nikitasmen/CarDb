import re
import webbrowser

_URL_RE = re.compile(r"^(https?://)[\w.-]+(?:\:[0-9]+)?(?:/.*)?$")

def validate_url(url):
    return isinstance(url, str) and bool(_URL_RE.match(url.strip()))

def open_url(url):
    if validate_url(url):
        webbrowser.open(url)
    else:
        raise ValueError("Invalid URL")
