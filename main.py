from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random
import json
import requests
from fake_useragent import UserAgent

# Function to introduce random delay
def random_delay():
    time.sleep(random.uniform(1, 5))

# Function to load the configuration from a JSON file
def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

# Get a random user agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Get a random proxy from the proxy list
def get_random_proxy(proxy_list):
    return random.choice(proxy_list)

# Load proxy list
def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

# Generic scraping function
def scrape_website(config, website, search_query, num_pages=5):
    results = []
    site_config = config[website]
    base_url = site_config["baseUrl"]
    url_template = site_config["urlTemplate"]
    selectors = site_config["selectors"]
    proxies = load_proxies('proxies.txt')  # Load proxies from file

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()
        
        for page_num in range(1, num_pages + 1):
            url = url_template.format(searchQuery=search_query, page=page_num)
            proxy = get_random_proxy(proxies)
            print('proxy...............................',proxy)
            context.set_extra_http_headers({"Proxy-Authorization": f"Basic {proxy}"})
            page.goto(url)
            
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            product_containers = soup.select(selectors["productContainer"])
            print('product_containers',product_containers)
            if not product_containers:
                print(f"No products found on page {page_num}")
                break
            
            for container in product_containers:
                title = container.select_one(selectors["title"]).get_text(strip=True)
                price = container.select_one(selectors["price"]).get_text(strip=True) if container.select_one(selectors["price"]) else 'N/A'
                link = base_url + container.select_one(selectors["link"])["href"]
                image = container.select_one(selectors["image"])["src"]
                results.append({'title': title, 'price': price, 'link': link, 'image': image})
            
            random_delay()
        
        browser.close()
    
    return results

# Function to save results to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
config = load_config('config.json')

# # Scrape Amazon
# amazon_results = scrape_website(config, 'amazon', 'clothing', num_pages=5)
# print('Length of Amazon results:', len(amazon_results))
# save_to_json(amazon_results, 'amazon_results.json')

# Scrape Nordstrom
nordstrom_results = scrape_website(config, 'nordstrom', 'dress', num_pages=5)
print('Length of Nordstrom results:', len(nordstrom_results))
save_to_json(nordstrom_results, 'nordstrom_results.json')

# Scrape ASOS
asos_results = scrape_website(config, 'asos', 'jeans', num_pages=5)
print('Length of ASOS results:', len(asos_results))
save_to_json(asos_results, 'asos_results.json')

# Scrape H&M
hm_results = scrape_website(config, 'hm', 'dress', num_pages=5)
print('Length of H&M results:', len(hm_results))
save_to_json(hm_results, 'hm_results.json')

# # Scrape Uniqlo
# uniqlo_results = scrape_website(config, 'uniqlo', 'jeans', num_pages=5)
# print('Length of Uniqlo results:', len(uniqlo_results))
# save_to_json(uniqlo_results, 'uniqlo_results.json')


# Scrape Nordstrom Rack
nordstrom_rack_results = scrape_website(config, 'nordstromrack', 'shoes', num_pages=5)
print('Length of Nordstrom Rack results:', len(nordstrom_rack_results))
save_to_json(nordstrom_rack_results, 'nordstrom_rack_results.json')

# Scrape Kohl's
kohls_results = scrape_website(config, 'kohls', 'dress', num_pages=5)
print('Length of Kohl\'s results:', len(kohls_results))
save_to_json(kohls_results, 'kohls_results.json')
