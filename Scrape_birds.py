import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_birds():

    if not os.path.exists('bird_images'):
        os.makedirs('bird_images')
    
    url = "https://www.doc.govt.nz/nature/native-animals/birds/birds-a-z/"
    
    print("Step 1: Fetching the main page...")
    try:
        response = requests.get(url)
        print(f"✓ Page loaded successfully (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to load page: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"✓ Page title: {soup.title.string if soup.title else 'No title found'}")
    
    print("step 2 : looking for birds")


    all_links = soup.find_all('doc-resizable-product-card')
    print(f"✓ Found {len(all_links)} total links on the page")
    
    bird_links = []
    
    for link in all_links:
        bird_name = link['title']
        bird_link = link['url']
       
       
       
        bird_links.append({
            'name': bird_name,
            'link': bird_link,
            'image_src': "",
            'alt_text': ""
        })
    
   


    print(bird_links)

    return bird_links


if __name__ == "__main__":
    bird_data = scrape_birds()