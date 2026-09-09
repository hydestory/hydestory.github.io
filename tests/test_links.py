"""Check local destinations and fragment anchors on the five primary pages."""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'src/note.html', 'src/activity.html', 'src/stock.html', 'src/50lan.html']

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for name in ('href', 'src'):
            if attrs.get(name):
                self.links.append(attrs[name])

class LocalLinks(unittest.TestCase):
    def test_primary_pages_have_real_destinations(self):
        for name in PAGES:
            page = ROOT / name
            for href in Page(page).links:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(page=name, href=href):
                    target = (ROOT / url.path.lstrip('/') if url.path.startswith('/') else page.parent / unquote(url.path)) if url.path else page
                    self.assertTrue(target.exists(), f'Missing destination: {target}')
                    if url.fragment and target.suffix == '.html':
                        self.assertIn(unquote(url.fragment), Page(target).ids)

if __name__ == '__main__':
    unittest.main()
