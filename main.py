from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random
import json

# Function to introduce random delay
def random_delay():
    time.sleep(random.uniform(1, 5))

# Function to scrape a page with Playwright
def scrape_page(url, selectors):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        print(content)
        soup = BeautifulSoup(content, 'html.parser')
        browser.close()
    return soup

# Function to scrape Macy's
def scrape_macys(num_pages=1):
    results = []
    config = {
        "urlTemplate": "https://www.macys.com/shop/featured/clothing",
        "selectors": {
            "mainContainer": "div.cell",
            "productContainer": "ul.items",
            "title": "div.productDetail > div.productDescription > a",
            "price": "div.productDetail > div.productDescription > div.priceInfo > span.price",
            "link": "div.productDetail > div.productDescription > a",
            "image": "div.productThumbnail >div.productThumbnailImage > a > div > picture > img"
        },
        "baseUrl": "https://www.macys.com",
        "nextPageDisabled": "li.a-disabled"
    }
    url_template = config['urlTemplate']
    selectors = config['selectors']

    for page_num in range(1, num_pages + 1):
        url = url_template
        soup = scrape_page(url, selectors)

        product_containers = soup.select(selectors['productContainer'])
        if not product_containers:
            print(f"No products found on page {page_num}")
            break

        for container in product_containers:
            title = container.select_one(selectors['title']).get_text(strip=True)
            price = container.select_one(selectors['price']).get_text(strip=True) if container.select_one(selectors['price']) else 'N/A'
            link = config['baseUrl'] + container.select_one(selectors['link'])['href']
            image = container.select_one(selectors['image'])['src']
            results.append({'title': title, 'price': price, 'link': link, 'image': image})

        random_delay()

    return results

# Function to scrape Etsy
def scrape_etsy(search_query, num_pages=1):
    results = []
    config = {
        "urlTemplate": "https://www.etsy.com/search?q={searchQuery}&page={page}",
        "selectors": {
            "mainContainer": "div[data-search-results-container]",
            "productContainer": "li.wt-list-unstyled",
            "title": ".v2-listing-card__title",
            "price": ".n-listing-card__price .currency-value",
            "link": "a.listing-link",
            "image": ".v2-listing-card__img img"
        },
        "nextPageDisabled": "nav[aria-label='Pagination'] li.disabled"
    }
    url_template = config['urlTemplate']
    selectors = config['selectors']

    for page_num in range(1, num_pages + 1):
        url = url_template.format(searchQuery=search_query, page=page_num)
        soup = scrape_page(url, selectors)

        product_containers = soup.select(selectors['productContainer'])
        if not product_containers:
            print(f"No products found on page {page_num}")
            break

        for container in product_containers:
            title = container.select_one(selectors['title']).get_text(strip=True)
            price = container.select_one(selectors['price']).get_text(strip=True) if container.select_one(selectors['price']) else 'N/A'
            link = container.select_one(selectors['link'])['href']
            image = container.select_one(selectors['image'])['src']
            results.append({'title': title, 'price': price, 'link': link, 'image': image})

        random_delay()

    return results

# Function to save results to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
macys_results = scrape_macys(num_pages=1)
save_to_json(macys_results, 'macys_results.json')

etsy_results = scrape_etsy(search_query='handmade necklace', num_pages=3)
save_to_json(etsy_results, 'etsy_results.json')

# Print results
for result in macys_results:
    print(result)

for result in etsy_results:
    print(result)
