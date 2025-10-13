import os
import requests

# Get the API key from the environment variable.
News_API = os.getenv("NEWS_API")

NEWS_URL = "https://newsapi.org/v2/top-headlines?sources=techcrunch"

def fetch_top_tech_news() -> None:
    """
    Get and show top headlines from News API.
    If something goes wrong, it will show US headlines.
    """
    params = {"apiKey": News_API}

    try:
        # Make a GET request to the news API.
        response = requests.get(NEWS_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as exc:
        # Print error if request fails.
        print(f"[Error] Failed to fetch news: {exc}")
        return

    articles = data.get("articles") or []
    if not articles:
        # Print message if no articles are found.
        print("No articles found.")
        return

    print("\n" + "=" * 60)
    print(f"Top Tech Headlines ({len(articles)} articles found)")
    print("=" * 60 + "\n")

    for idx, article in enumerate(articles, start=1):
        source = article.get("source", {}).get("name", "Unknown Source")
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")

        # Print each article's details.
        print(f"{idx}. {title}")
        print(f"   Source      : {source}")
        print(f"   Description : {description}")
        print("-" * 60)

    print("\nEnd of feed.\n" + "=" * 60)

if __name__ == "__main__":
    fetch_top_tech_news()
