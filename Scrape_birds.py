import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import os
from urllib.parse import urljoin
import time

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

    if bird_links:
        print("\n ALL BIRDS FOUND:")
        print("=" * 50)
        for i, bird in enumerate(bird_links, 1):
            print(f"{i:2d}. {bird['name']}")
            print(f"    Link: {bird['link']}")
            print(f"    Image: {bird['image_src']}")
            print()
    else:
        print("✗ No bird links found. Let's debug further")
        

        links_with_images = []
        for link in all_links:
            images_in_link = link.find_all('img')
            if images_in_link:
                href = link.get('href')
                alt = images_in_link[0].get('alt', 'No alt text')
                links_with_images.append((alt, href))
        
        print(f"\nDEBUG: Found {len(links_with_images)} links containing images:")
        for i, (alt, href) in enumerate(links_with_images):
            print(f"  {i+1:2d}. '{alt}' -> '{href}'")
    
    return bird_links

if __name__ == "__main__":
    bird_data = scrape_birds()