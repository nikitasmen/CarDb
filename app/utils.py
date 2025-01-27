import webbrowser

def open_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        webbrowser.open(url)
    else:
        raise ValueError("Invalid URL")
