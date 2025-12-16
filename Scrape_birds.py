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

    parent = soup.find_all('doc-resizable-product-card')


   

    all_links = soup.find_all('doc-resizable-product-card')
    print(f"✓ Found {len(all_links)} total links on the page")
  
    
    bird_links = []
    bird_image_urls = []

    for img in parent:
        bird_image = img.find('doc-image')['src']

        bird_image_urls.append({
            'image': bird_image
        })
    
    for link in all_links:
        bird_name = link['title']
        bird_link = link['url']
        bird_image = bird_image_urls[0]['image'] if bird_image_urls else ""


        bird_links.append({
            'name': bird_name,
            'link': bird_link,
            'image': bird_image
        })

    

    return bird_links

scrape_birds()


def save_to_csv(bird_data):
    df = pd.DataFrame(bird_data)
    df.to_csv('bird_data.csv', index=False)
    print("Bird data saved to 'bird_data.csv'")

save_to_csv(scrape_birds())