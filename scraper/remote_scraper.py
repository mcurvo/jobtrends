# scraper/remote_scraper.py
import requests
import pandas as pd

def fetch_remoteok_jobs():
    """
    Fetches the latest jobs from the RemoteOK API and returns
    a DataFrame with the fields we need.
    """
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    data = resp.json()
    # The first element is metadata; actual jobs start at index 1
    jobs = data[1:]

    # Convert to DataFrame
    df = pd.DataFrame(jobs)
    # Keep only relevant columns (ensure these exist in the JSON)
    df = df.rename(columns={
        "company": "company",
        "position": "position",
        "location": "location",
        "tags": "tags",
        "description": "description",
        "url": "url",
        "date": "date"
    })
    # Use the 'tags' field as raw skills
    df["skills"] = df["tags"].apply(lambda x: x if isinstance(x, list) else [])

    return df[["company", "position", "location", "tags", "description", "url", "skills", "date"]]
