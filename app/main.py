import time
import requests
from bs4 import BeautifulSoup

webpage = "https://luckyelk.com/collections/thca-aa-mid-shelf"

def get_html(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "en-US,en;q=0.5",
        'Referer': "https://luckyelk.com/collections/thca-aaaa-exotic",
        'Dnt': "1",
        'Connection': "keep-alive",
        'Upgrade-Insecure-Requests': "1",

    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Connection was successful: Scraping - {url} - Please wait...")
        time.sleep(3)
        page_soup = BeautifulSoup(response.text, "lxml")
        return page_soup
    else:
        print(f"Connection was Unsuccessful: {response.status_code}")

soup = get_html(webpage)
sale_items = []

if soup:
    # Get Price Containers
    price_containers = soup.find_all("div", class_="price")
    # Get Strain Names
    strain_names = soup.find_all("span", attrs={"data-product-title": True})

    # Looking for sales!
    for strain, container in zip(strain_names, price_containers):
        strain_name = strain.get('data-product-title').strip()

        if 'price--on-sale' in container.get('class'):
            sale_price = container.find('span',class_='price-item--sale')
            if sale_price:
                sale_price = sale_price.get_text().strip()
                sale_price_value = sale_price.replace('From', '').replace('USD', '')
                sale_items.append({'Strain:': strain_name, 'Price:': sale_price_value, 'On Sale?': True })

        # If it's not on sale that's ok
        else:
            regular_price = container.find('span',class_='price-item--regular')
            if regular_price:
                regular_price = regular_price.get_text().strip()
                regular_price_value = regular_price.replace('From', '').replace('USD', '')
                sale_items.append({'Strain:': strain_name, 'Price:': regular_price_value, 'On Sale?': False})

    for item in sale_items:
        if item ['On Sale?']:
            print(f"🍁 SALE! - {item['Strain:']} - {item['Price:']} 🍁")
        else:
            print(f"😶 {item['Strain:']} - {item['Price:']} 😶")