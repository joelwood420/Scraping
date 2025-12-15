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
        response.raise_for_status()
        print(f"✓ Page loaded successfully (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to load page: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"✓ Page title: {soup.title.string if soup.title else 'No title found'}")
    
    print("\nStep 2: Looking for <a> tags containing <img> tags")
    
   
    all_links = soup.find_all('a', href=True)
    print(f"✓ Found {len(all_links)} total links on the page")
    
    bird_links = []
    
    for link in all_links:
        
        images_in_link = link.find_all('img')
        
        if images_in_link:  
            href = link.get('href')
            
            
            img = images_in_link[0]
            alt_text = img.get('alt', '').strip()
            img_src = img.get('src', '')
            
    
            if href and href != url and href != '#' and alt_text and len(alt_text) > 2:
                skip_words = ['logo', 'menu', 'search', 'facebook', 'twitter', 'instagram', 'youtube', 'back to top']
                if not any(skip_word in alt_text.lower() for skip_word in skip_words):
                    bird_name = alt_text
                    full_url = urljoin(url, href)
                    
                    bird_links.append({
                        'name': bird_name,
                        'link': full_url,
                        'image_src': img_src,
                        'alt_text': alt_text
                    })
    
    print(f"\n✓ Found {len(bird_links)} potential bird links with images")
    
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