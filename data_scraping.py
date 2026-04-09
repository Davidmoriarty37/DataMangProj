import requests
import pandas as pd

# Bearer token for X API authentication
BEARER_TOKEN = "EnterTokenHere"

# Base URL for X recent search endpoint
BASE_URL = "https://api.x.com/2/tweets/search/recent"

# List of companies and their X handles
companies = [
    {"name": "Comcast", "handles": ["XfinitySupport", "comcast"]},
    {"name": "Uber", "handles": ["Uber", "Uber_Support"]},
    {"name": "Delta", "handles": ["Delta"]},
    {"name": "Amazon", "handles": ["AmazonHelp"]},
    {"name": "AT&T", "handles": ["ATT", "ATTHelp"]},
]

# This searches for the company name or handle, and only keeps English posts, and removes retweets
def build_query(company):
    handle_part = " OR ".join([f"@{h}" for h in company["handles"]])
    return f'("{company["name"]}" OR {handle_part}) lang:en -is:retweet'

# This pulls up to 50 posts for a given query
def search_posts(query):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = {
        "query": query,
        "max_results": 50,
        "tweet.fields": "created_at,author_id,public_metrics"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    data = response.json()

    rows = []

    for tweet in data.get("data", []):
        rows.append({
            "id": tweet["id"],
            "date": tweet.get("created_at"),
            "author_id": tweet.get("author_id"),
            "text": tweet.get("text"),
            "like_count": tweet.get("public_metrics", {}).get("like_count"),
            "reply_count": tweet.get("public_metrics", {}).get("reply_count"),
            "retweet_count": tweet.get("public_metrics", {}).get("retweet_count"),
            "quote_count": tweet.get("public_metrics", {}).get("quote_count"),
        })

    return rows

# Collect posts from all companies and add the company name to each row
all_data = []

for company in companies:
    query = build_query(company)
    rows = search_posts(query)

    for row in rows:
        row["company"] = company["name"]
        all_data.append(row)

# Turn the data into a DataFrame and save it as a CSV file
df = pd.DataFrame(all_data)
df.to_csv("tweets.csv", index=False)