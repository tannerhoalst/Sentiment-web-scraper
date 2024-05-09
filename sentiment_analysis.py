from textblob import TextBlob
import pymongo

# MongoDB configuration
MONGODB_URI = "mongodb://localhost:27017/news_database"
DB_NAME = "news_database"
COLLECTION_NAME = "headlines"

# Function to connect to MongoDB and retrieve headlines
def get_headlines_from_mongodb():
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Retrieve headlines from MongoDB documents
        headlines = [headline['headline_text'] for headline in collection.find()]
        
        client.close()
        return headlines
    except pymongo.errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

# Function to perform sentiment analysis on headlines
def perform_sentiment_analysis(headlines):
    sentiment_scores = []
    for headline in headlines:
        blob = TextBlob(headline)
        sentiment_score = blob.sentiment.polarity
        sentiment_scores.append((headline, sentiment_score))
    return sentiment_scores

# Example usage
if __name__ == "__main__":
    # Get headlines from MongoDB
    headlines = get_headlines_from_mongodb()
    
    # Perform sentiment analysis
    sentiment_scores = perform_sentiment_analysis(headlines)
    
    # Print sentiment scores
    for headline, score in sentiment_scores:
        print(f"Headline: {headline}, Sentiment Score: {score}")
