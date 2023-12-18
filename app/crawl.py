import re
from pathlib import Path
from urllib.parse import urlparse

import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

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

        # Sanitize the url and remove the 'https_' prefix
        sanitized_url = re.sub(r"\W+", "_", response.url)
        sanitized_url = sanitized_url.replace("https_", "", 1)

        page_path = self.domain_path / f"{sanitized_url}.txt"

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


def crawl_webpage(start_url):
    process = CrawlerProcess()
    process.crawl(MySpider, start_url=start_url)
    process.start()


def create_master_file(start_url: str):
    domain_path = OUTPUT_DIR / urlparse(start_url).netloc.replace(".", "_")
    master_file_path = (
        domain_path
        / f"{urlparse(start_url).netloc.replace('.', '_')}_master_combined.txt"
    )
    with open(master_file_path, "w", encoding="utf-8") as master_file:
        for txt_file in domain_path.iterdir():
            if txt_file.suffix == ".txt":
                with open(txt_file, "r", encoding="utf-8") as file:
                    master_file.write(file.read())


def crawl_and_combine(start_url):
    # Crawl the website
    crawl_webpage(start_url)

    # After the crawl, combine all text files into a master file
    create_master_file(start_url)


# Example usage
# run_spider('https://astelmach01.github.io/tinylang')
