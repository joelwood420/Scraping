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

    all_birds = soup.find_all('doc-resizable-product-card')
    if not all_birds:
        print("✗ No bird links found on the page")
        return
    print(f"✓ Found {len(all_birds)} total links on the page")


    bird_images = []
    bird_names = []

    for img in all_birds:
        bird_image = img.find('doc-image')['src']

        bird_images.append({
            'image': bird_image
        })

    for name in all_birds:
        bird_name = name['title']
        bird_image = bird_images[0]['image'] if bird_images else ""


        bird_names.append({
            'name': bird_name,
            'image': bird_image
        })

    

    return bird_names



def save_to_csv(bird_data):
    df = pd.DataFrame(bird_data)
    df.to_csv('bird_data.csv', index=True)
    print("Bird data saved to 'bird_data.csv'")

save_to_csv(scrape_birds())