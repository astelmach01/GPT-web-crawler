import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re


from . import OUTPUT_DIR


def get_last_url_segment(url):
    # Split the URL and filter out empty segments
    url_segments = [segment for segment in url.split("/") if segment]
    # Extract the last segment or use a default identifier
    return url_segments[-1] if url_segments else "root"


class MySpider(scrapy.Spider):
    name = "myspider"

    def __init__(self, start_url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        parsed_url = urlparse(start_url)
        self.domain = parsed_url.netloc
        # Create a directory for this domain
        self.domain_path = OUTPUT_DIR / self.domain.replace(".", "_")
        self.domain_path.mkdir(parents=True, exist_ok=True)

    def parse(self, response):
        self.log(f"Visited {response.url}")

        # split the url into /
        last_segment = get_last_url_segment(response.url)

        # Write response to a file
        page_path = self.domain_path / f"{last_segment}.txt"

        with open(page_path, "w", encoding="utf-8") as file:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            cleaned_text = re.sub("\n\s*\n", "\n", text)
            file.write(cleaned_text)
        # Follow links
        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)
            if self.domain in url:
                yield scrapy.Request(url, callback=self.parse)


def run_spider(start_url):
    process = CrawlerProcess()
    process.crawl(MySpider, start_url=start_url)
    process.start()


# Example usage
# run_spider('https://astelmach01.github.io/tinylang')
