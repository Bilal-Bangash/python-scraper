from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random
import json

# Function to introduce random delay
def random_delay():
    time.sleep(random.uniform(1, 5))

# Function to load the configuration from a JSON file
def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

# Generic scraping function
def scrape_website(config, website, search_query, num_pages=5):
    results = []
    site_config = config[website]
    base_url = site_config["baseUrl"]
    url_template = site_config["urlTemplate"]
    selectors = site_config["selectors"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for page_num in range(1, num_pages + 1):
            url = url_template.format(searchQuery=search_query, page=page_num)
            page.goto(url)
            
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            product_containers = soup.select(selectors["productContainer"])
            if not product_containers:
                print(f"No products found on page {page_num}")
                break
            
            for container in product_containers:
                title_element = container.select_one(selectors["title"])
                price_element = container.select_one(selectors["price"])
                link_element = container.select_one(selectors["link"])
                image_element = container.select_one(selectors["image"])

                title = title_element.get_text(strip=True) if title_element else 'N/A'
                price = price_element.get_text(strip=True) if price_element else 'N/A'
                link = base_url + link_element["href"] if link_element else 'N/A'
                
                # Check if the image is in an img tag or a style attribute
                image_url = 'N/A'
                if image_element:
                    if image_element.name == 'img':
                        image_url = image_element.get('src', 'N/A')
                    elif image_element.get("style"):
                        image_style = image_element.get("style")
                        if "url('" in image_style:
                            image_url = image_style.split("url('")[1].split("')")[0]
                
                results.append({'title': title, 'price': price, 'link': link, 'image': image_url})
            
            random_delay()
        
        browser.close()
    
    return results

# Function to save results to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
config = load_config('config.json')

# Scrape Amazon
# amazon_results = scrape_website(config, 'amazon', 'clothing', num_pages=5)
# print('Length of Amazon results:', len(amazon_results))
# save_to_json(amazon_results, 'amazon_results.json')

# # Scrape Nordstrom
# nordstrom_results = scrape_website(config, 'nordstrom', 'dress', num_pages=5)
# print('Length of Nordstrom results:', len(nordstrom_results))
# save_to_json(nordstrom_results, 'nordstrom_results.json')

# # Scrape ASOS
# asos_results = scrape_website(config, 'asos', 'jeans', num_pages=5)
# print('Length of ASOS results:', len(asos_results))
# save_to_json(asos_results, 'asos_results.json')

# # Scrape H&M
# hm_results = scrape_website(config, 'hm', 'dress', num_pages=5)
# print('Length of H&M results:', len(hm_results))
# save_to_json(hm_results, 'hm_results.json')

# # # Scrape Uniqlo
# # uniqlo_results = scrape_website(config, 'uniqlo', 'jeans', num_pages=5)
# # print('Length of Uniqlo results:', len(uniqlo_results))
# # save_to_json(uniqlo_results, 'uniqlo_results.json')


# # Scrape Nordstrom Rack
# nordstrom_rack_results = scrape_website(config, 'nordstromrack', 'shoes', num_pages=5)
# print('Length of Nordstrom Rack results:', len(nordstrom_rack_results))
# save_to_json(nordstrom_rack_results, 'nordstrom_rack_results.json')

# # Scrape Kohl's
# kohls_results = scrape_website(config, 'kohls', 'dress', num_pages=5)
# print('Length of Kohl\'s results:', len(kohls_results))
# save_to_json(kohls_results, 'kohls_results.json')


# Scrape Alpha Industries
# alpha_industries_results = scrape_website(config, 'alphainsutries', 'jeans', num_pages=5)
# print('Length of Alpha Industries results:', len(alpha_industries_results))
# save_to_json(alpha_industries_results, 'alpha_industries_results.json')

# Scrape POC NYC
pocnyc_results = scrape_website(config, 'pocnyc', 'jeans', num_pages=5)
print('Length of POC NYC results:', len(pocnyc_results))
save_to_json(pocnyc_results, 'pocnyc_results.json')