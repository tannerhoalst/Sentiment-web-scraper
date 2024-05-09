import requests
from bs4 import BeautifulSoup
import pymongo

# MongoDB configuration
MONGODB_URI = "mongodb://localhost:27017/news_database"
DB_NAME = "news_database"
COLLECTION_NAME = "headlines"

# List of news websites to scrape
websites = [
    {'name': 'ZeroHedge', 'url': 'https://www.zerohedge.com/', 'headline_tag': 'h2'},
    {'name': 'The Guardian', 'url': 'https://www.theguardian.com/international', 'headline_tag': 'h3'},
]

# Function to connect to MongoDB
def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        return collection
    except pymongo.errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

# Function to scrape headlines from a given website URL and store in MongoDB
def scrape_headlines(website):
    print(f"Scraping headlines from {website['name']}...")
    try:
        response = requests.get(website['url'])
        response.raise_for_status()  # Raise HTTPError for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        headlines = [headline.text.strip() for headline in soup.find_all(website['headline_tag'])]

        collection = connect_to_mongodb()

        for headline_text in headlines:
            existing_headline = collection.find_one({'headline_text': headline_text})
            if existing_headline is None:
                headline_data = {
                    'website': website['name'],
                    'headline_text': headline_text
                }
                collection.insert_one(headline_data)
                print(f"Inserted headline: {headline_text}")
            else:
                print(f"Duplicate headline found: {headline_text}. Skipping...")

        print(f"Stored {len(headlines)} headlines from {website['name']} in MongoDB.")
    except (requests.exceptions.RequestException, pymongo.errors.PyMongoError) as e:
        print(f"Error while scraping {website['name']}: {e}")

# Scrape headlines from each website in the list
for site in websites:
    scrape_headlines(site)
    print()  # Add a blank line for readability between websites

# mongod --dbpath ./data
# /usr/local/bin/python3 webscraper.py