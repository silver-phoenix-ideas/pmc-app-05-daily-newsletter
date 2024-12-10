# Imports
import os
import sys
import dotenv
import smtplib
import requests
import datetime
import modules.email_utils as email_utils

# Configurations
dotenv.load_dotenv(".env")
topic = "Disney Sales"
language = "en"
start_date = datetime.datetime.now() - datetime.timedelta(1)
sort_by = "relevancy"
endpoint = "https://newsapi.org/v2/everything"
params = {
    "q": topic,
    "language": language,
    "from": start_date,
    "sortBy": sort_by,
    "apiKey": os.getenv("NEWS_API_KEY")
}

# Request
response = requests.get(endpoint, params)
content = response.json()

print()

# Exit if No Results
if not content["articles"]:
    print("Newsletter not sent.")
    print("There are no articles.")
    sys.exit()

# Newsletter
newsletter = f"Daily {topic} Newsletter\n\n"

for article in content["articles"]:
    if article["source"]["name"] == "[Removed]":
        continue

    title = article["title"] or "[Missing Title]"
    description = article["description"] or "[Missing Description]"
    url = article["url"] or "[Missing URL]"
    newsletter += f"{title}\n{description}\nRead More: {url}\n\n"

# Send to Email
try:
    email_utils.send_newsletter(topic, newsletter)
    print("Newsletter sent successfully.")

except smtplib.SMTPResponseException as e:
    print("Newsletter couldn't be sent.")

    match e.smtp_code:
        case 334:
            print("Authentication credentials missing.")
        case 535:
            print("Authentication credentials invalid.")

except smtplib.SMTPRecipientsRefused as e:
    print("Newsletter couldn't be sent.")
    print("Recipient address invalid.")
