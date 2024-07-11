from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random
import json

# Function to introduce random delay
def random_delay():
    time.sleep(random.uniform(1, 5))

# Main scraping function
def scrape_amazon(search_query, num_pages=1):
    results = []
    base_url = "https://www.amazon.com/s"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for page_num in range(1, num_pages + 1):
            url = f"{base_url}?k={search_query}&page={page_num}"
            page.goto(url)
            
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            product_containers = soup.select('div.s-main-slot > div[data-component-type="s-search-result"]')
            if not product_containers:
                print(f"No products found on page {page_num}")
                break
            
            for container in product_containers:
                title = container.select_one('h2 a span').get_text(strip=True)
                price = container.select_one('.a-price > .a-offscreen').get_text(strip=True) if container.select_one('.a-price > .a-offscreen') else 'N/A'
                link = "https://www.amazon.com" + container.select_one('h2 a')['href']
                image = container.select_one('img.s-image')['src']
                results.append({'title': title, 'price': price, 'link': link, 'image': image})
            
            random_delay()
        
        browser.close()
    
    return results

# Function to save results to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
search_query = "laptop"
results = scrape_amazon(search_query, num_pages=3)

# Save results to a JSON file
save_to_json(results, 'amazon_results.json')
