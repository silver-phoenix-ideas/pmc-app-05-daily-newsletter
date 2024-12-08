import os
import requests

topic = "Disney Sales"
language = "en"
start_date = "2024-12-07"
sort_by = "relevancy"
endpoint = "https://newsapi.org/v2/everything"
params = {
    "q": topic,
    "language": language,
    "from": start_date,
    "sortBy": sort_by,
    "apiKey": os.getenv("NEWS_API_KEY")
}

response = requests.get(endpoint, params)
content = response.json()

for article in content["articles"]:
    print("\n" + article["title"])
